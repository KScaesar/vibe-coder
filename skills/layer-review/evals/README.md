# Evals

`package_skill.py` 排除整個 `evals/`，這裡的內容不會進到 skill 的載入預算。

目前只有 `evals.json`（產出品質），測「skill 叫起來之後，報告對不對」。尚未建立觸發 eval（`trigger_eval.json`）。

## 結構

```
evals/
├── evals.json              # 3 個案例 + assertions
├── files/
│   └── setup_fixture.sh    # 產生測試用的 Go 訂單服務 repo
└── README.md
```

## Fixture

`files/setup_fixture.sh <target-dir> [--dirty]` 建一個有三個 commit 的小型 Go repo，第二個 commit 刻意埋入：

| 問題 | 位置 | 應歸屬 layer |
|---|---|---|
| `fmt.Sprintf` 拼 SQL（SQL injection） | `infra/order_repo.go` | Infrastructure |
| 逐筆查 `order_items`（N+1） | `infra/order_repo.go` | Infrastructure |
| VIP 折扣規則寫在 handler | `httpapi/handler.go` | User Interface |
| domain 依賴 `database/sql`、`log` | `domain/order.go` | Domain |
| 只有單一實作的 factory 抽象 | `domain/` + `infra/` | Domain / Infrastructure |

`--dirty` 另外留下未 commit 的 `app/place_order.go` 改動：開了 transaction 但沒傳給 `Save`，錯誤路徑也沒有 rollback。

每個 run 都要用自己的 fixture 副本，因為報告會寫進 repo 的工作目錄。

## 案例

| id | prompt | 測什麼 |
|---|---|---|
| 1 | `HEAD~2..HEAD`，`detail=true` | 分層歸類、埋入問題是否被抓到、metadata 與檔名、File Change Summaries |
| 2 | 未 commit 的改動 | 範圍判斷（只審 working tree）、時間戳檔名、無 detail 時不附逐檔摘要 |
| 3 | 不存在的 commit | 只輸出 `## Error`，不產空殼報告、不擅自改範圍 |

## 執行方式

在 Claude Code 裡請 Claude 用 skill-creator 流程跑這份 eval，例如：

> 用 skill-creator 跑 skills/layer-review 的 evals，baseline 用 without_skill

流程重點（skill-creator 會照做，列出來方便檢查）：

1. 每個案例 × `with_skill` / `without_skill` 各建一份 fixture，放在 skill-creator 的 workspace（建議放 scratchpad，不要進 repo）：

   ```
   layer-review-workspace/iteration-N/
   └── eval-<id>-<name>/
       ├── eval_metadata.json
       ├── with_skill/
       │   ├── repo/            # fixture
       │   └── run-1/
       │       ├── outputs/     # 報告副本
       │       ├── grading.json
       │       └── timing.json
       └── without_skill/ ...
   ```

   `aggregate_benchmark` 只認 `run-*/` 底下的檔案，少了這層會全部算成 0。

2. 同一輪一次派出全部 subagent，完成通知裡的 `total_tokens` / `duration_ms` 當下寫進 `timing.json`，事後拿不到。
3. 依 `evals.json` 的 assertions 評分，寫入 `grading.json`（欄位必須是 `text` / `passed` / `evidence`）。
4. 彙整與檢視（在 skill-creator 目錄下）：

   ```bash
   uv run --no-project python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name layer-review
   uv run --no-project python eval-viewer/generate_review.py <workspace>/iteration-N \
     --skill-name layer-review --benchmark <workspace>/iteration-N/benchmark.json \
     --static <workspace>/iteration-N/review.html
   ```

   不加 `--static` 會啟動本機 server 並自動開瀏覽器；加了只產出 HTML 檔，自己打開即可。第二輪之後加 `--previous-workspace <workspace>/iteration-<N-1>` 可對照上一輪。

沒有環境跑 subagent 時，也可以手動：跑 `setup_fixture.sh`、在 fixture 目錄下照 prompt 執行，逐條核對 assertions。

## 判讀

第一輪結果（2026-09-23，每組各 1 次）：with_skill 100%、without_skill 64%，耗時 +10s、tokens +2.8k。

- **內容類 assertions 區辨力低。** 兩組都抓到了全部埋入的問題，差距幾乎全來自格式（檔名、`datetime`/`scope`、依 layer 分組、`./` 路徑、`## Error`）。改 SKILL.md 後若只有內容類 assertion 在動，代表 fixture 太簡單，應該埋更隱蔽的問題（例如跨 layer 的間接影響），而不是加更多格式檢查。
- **案例 3 幾乎不區辨。** baseline 同樣會停下來說明 commit 不存在，只差標題不是 `## Error`。可考慮換成「old 存在、new 不存在」或「hash 可解析但範圍為空」這類更容易被硬做下去的情境。
- **看 transcript，不只看分數。** 例如 with_skill 會用 `gopls references` 確認 symbol 引用、並把 repo 內無法確認的事標成「需要確認」，這些是 skill 想要的行為，但目前沒有 assertion 覆蓋。
- 每組只跑 1 次，變異量看不出來；要下結論前至少各跑 3 次。

第三輪（2026-09-23，加入「篇幅中等、儘可能列出所有問題」後，with_skill 各跑 3 次；案例 1、2 各新增覆蓋率 assertions）：

- 案例 1：14/15、14/15、15/15。唯一不穩定的是「缺 response DTO」（1/3），其餘低嚴重度項目（IDOR、輸入驗證、`itemRows.Err()`）3/3。
- 案例 2：3 次皆 10/10。
- 篇幅：案例 1 約 6100–6600 字、案例 2 約 3600–4400 字，沒有因為要求列全而回漲到第一輪的長度。
- 耗時約 190–280s，比第一輪（80–110s）長，tokens 幾乎不變，原因尚未確認。
- 其中一次案例 2 把範圍外的既有問題寫成獨立的 `## Domain Layer（周邊既有問題）` 等段落；有標示非本次 diff，但若要嚴格限縮範圍，需在 SKILL.md 說明既有問題該放哪裡。
