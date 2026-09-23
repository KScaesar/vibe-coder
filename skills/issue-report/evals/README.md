# Evals

`package_skill.py` 排除整個 `evals/`，這裡的內容不會進到 skill 的載入預算。

兩份 eval 測不同的東西，缺一不可：`trigger_eval.json` 測「skill 有沒有被叫起來」，`evals.json` 測「叫起來之後產出對不對」。前者過了不代表後者會過。

## evals.json — 產出品質

四個案例，每個附可驗證的 expectations，schema 見 skill-creator 的 `references/schemas.md`。

| id | 測什麼 |
|---|---|
| 1 | 資料管線情境、Observations 的選用、檔案輸出 |
| 2 | 資訊不足時改為提問，不產骨架也不捏造 |
| 3 | 多現象拆單、推測與現象分離 |
| 4 | 中間地帶的重現機率、Summary 精度高於標題 |

用 skill-creator 的 eval 流程執行（會起 subagent 實跑並由 grader 評分）：

```bash
python -m scripts.run_loop --skill-path <path/to/issue-report>
```

沒有環境可跑自動化時，這四個案例也可以人工執行，逐條核對 expectations。

## trigger_eval.json — 觸發準確率

只測 frontmatter description 決定的觸發行為，不看產出內容。

```bash
python -m scripts.run_eval \
  --eval-set evals/trigger_eval.json \
  --skill-path . \
  --runs-per-query 5 \
  --verbose
```

預設 `--runs-per-query 3` 的取樣對於判斷 0.8 通過率太少，建議 5 次以上。

正例 10 筆、負例 10 筆。負例對應 description 明列的四類邊界：debug 與找成因、postmortem 與 RCA、PR 說明與 release note、功能需求。這四類最容易誤觸發，因為它們同樣以「系統出了問題」開場。

**判讀注意**：最接近的一組是負例「這個 504 可能是什麼原因造成的」與正例「這個 bug 回報一下，session API 一直回 504」——前者要解釋，後者要開單。若負例誤觸發，不要直接往 description 加負面敘述，那通常會把正例一起壓下去；改成強化正例的共同特徵（明確的移交對象、明確的產出格式要求）。

目標：正負例皆 ≥ 0.8 通過率。
