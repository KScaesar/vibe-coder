---
name: handoff
description: 把目前工作壓縮成「交接文件 (handoff document)」，讓沒有記憶的下一個 agent（新 session、被壓縮後的同一 session、另一個 agent）能安全接手；同時會偵測並沿用專案現有的狀態紀錄 (state artifacts)，例如進度、現況、決策、規則、任務清單。當使用者輸入 /handoff、要求「寫交接」「整理給下個 session」「關掉前存 context」，或由 hook／context 門檻自動觸發時使用；不用於一般對話摘要 (chat summary)。
argument-hint: "[下一步要做的事] [--auto]"
disable-model-invocation: false
---

# Handoff

把目前的工作狀態，送過 session 邊界。

> 交接不是聊天摘要 (chat summary)，也不是知識庫 (knowledge base)。它回答一個問題：**下一輪現在可以怎麼安全繼續？**

做法：先找出專案已有的狀態載體 (state artifacts) 並沿用，再產出一份短交接，把其餘資訊指向它們。

## 用法 (Usage)

```
/handoff                              手動，下一步由 skill 依對話最後的狀態推斷
/handoff 接著實作 retry 機制            手動，指定下一個 session 要做的事
/handoff --auto                       自動模式，無人在場，不提問
/handoff --auto 接著實作 retry 機制     自動模式，並指定下一步
```

| 參數 | 說明 |
|---|---|
| `[下一步要做的事]` | 選填。自由文字，交接會以它為主軸，並寫進 NEXT ACTION |
| `--auto` | 選填。給 hook 或 context 門檻自動觸發用：不提問、只寫允許的檔案、輸出交接全文供程式擷取（細節見第五節）。手動使用不需要加 |

本次傳入的參數：`$ARGUMENTS`

判讀方式：參數含 `--auto` 就進入自動模式（第五節）；去掉 `--auto` 後剩下的文字就是「下一步要做的事」；沒有參數就依對話最後的狀態推斷。

## 一、核心原則 (Core Principles)

1. **權威順序 (order of authority)**：機器可驗證的事實 (machine-verifiable facts，如版本控制、測試、環境) > 長期文件 (durable docs，如現況、決策、規格) > 交接文件 > 對話。交接文件只提供「從哪裡開始查證」的方向，不是真相本身，會過期。
2. **引用，不複製 (reference, don't copy)**：規格 (spec)、計畫 (plan)、決策紀錄 (decision log)、追蹤項目 (issue)、變更紀錄 (change history) 已存在就給路徑或連結。能由版本控制 (version control) 或測試重新算出的事實，不要另寫副本。
3. **重「為什麼」，輕「做了什麼」 (why over what)**：變更紀錄已記錄做了什麼；交接補的是動機 (rationale)、被比較過的備選 (alternatives considered)、被排除的方案 (rejected options)、未驗證的假設 (unverified assumptions)。探索過程丟掉，只留結論與其理由。
4. **證據要分級 (graded evidence)**：每個「完成」都標明是哪一級（見下表）。不要只寫 Done。
5. **缺漏要看得見 (make gaps visible)**：每個欄位都要填。沒有就寫「無」，沒討論過就寫「未討論」，不要整段省略，也不要編造。已知的未知 (known unknowns) 交給接手者，避免被誤讀成「不存在」。
6. **一個下一步 (one next action)**：給接手者第一個具體、安全的動作，不是 TODO 清單。
7. **每項一行，約 80 行內 (one line per item)**：細節放連結。超過就把內容升級 (promote) 到長期文件。
8. **遮蔽敏感資訊 (redact secrets)**：API key、密碼、token、個資一律寫 `[REDACTED]`。
9. **每類資訊只有一個正本 (single source of truth)**：不要為了交接另開平行的狀態、記憶或最新版檔案。

| 證據標籤 (evidence tag) | 意義 |
|---|---|
| `[verified]` | 本輪實際執行過，附指令與結果 |
| `[claimed]` | 上游或舊文件宣稱，本輪未重跑 |
| `[inferred]` | 由閱讀 code／文件推論，未執行 |
| `[unverified]` | 明確尚未驗證 |

## 二、先找出狀態載體，有什麼就用什麼 (Detect and Reuse State Artifacts)

動筆前，檢查專案裡有哪些載體在承擔下列角色，不論檔名或工具為何，都依角色沿用。沒有的不要為了交接而新建，除非任務確實需要。

| 載體角色 (artifact role) | 怎麼用 |
|---|---|
| 可驗證項目清單 (verifiable checklist，每項有通過與否) | 只有端到端驗證 (end-to-end verification) 後才標為通過；不刪除、不改寫項目描述；NEXT ACTION 挑優先度最高且未通過的一項，一次只做一項。清單用結構化格式 (structured format) 比自由文字穩定，較不容易被誤改，但這只降低風險，不是保證 |
| 附加式進度紀錄 (append-only progress log) | 只往後追加簡短紀錄：做了什麼、卡在哪、下一步；不改寫舊紀錄 |
| 覆寫式現況文件 (overwrite-only current-state doc) | 只寫「現在的狀態與下一步」，覆寫而不累積，不寫成流水帳 (running diary) |
| 決策紀錄 (decision log) | 已確認或已否決的決策，連同理由與備選一起記錄 |
| 長期規則文件 (standing rules doc) | 只放長期有效的工作規則；只對這一輪有用的不要放 |
| 規格、計畫、追蹤項目 (spec / plan / issue) | 在交接中引用路徑或連結，不重寫其內容 |
| 版本控制與測試 (version control & tests) | 取得目前版本、分支、未提交變更 (uncommitted changes)、測試結果，作為證據與接手時的比對基準。不要擅自提交 (commit) 或推送 (push)；有未提交的變更，就如實寫進 `working_tree` 與 STATE |

更新既有載體後，在回報中列出改了哪些。自動模式 (`--auto`) 下的限制見第五節。

## 三、撰寫步驟 (Writing Steps)

1. **偵測 (detect)**：依第二節掌握可沿用的載體與既有產物路徑。
2. **取得版本事實 (get revision facts)**：目前版本、分支、未提交變更（Git 為例：`git rev-parse HEAD`、`git branch --show-current`、`git status --short`）。沒有版本控制就寫 `none`。
3. **萃取 (extract)**：依模板逐欄填寫。
4. **對齊下一步 (align next action)**：有使用者參數就以它為主軸；沒有就用對話最後的狀態推斷。
5. **敏感資訊檢查 (secrets check)**：全文過一遍。
6. **升級判斷 (promotion check)**：見第六節，能升級的就升級，交接裡留連結。
7. **存檔並回報 (save and report)**：回報絕對路徑，不重貼全文（`--auto` 例外）。

### 儲存位置 (Storage Location)

預設在目前工作目錄的 `handoff/`，使用者指定路徑則以指定為準。檔名含任務 slug 與時間戳 (timestamp)，例如 `handoff-rate-limiter-20261009-1430.md`，避免覆蓋。可提醒使用者不要把這個目錄納入版本控制。

### 模板 (Template)

```markdown
---
generated_at: <ISO 時間>
repo: <路徑或名稱>
branch: <branch>
base_revision: <產生交接時的版本，例如 commit sha；沒有則 none>
working_tree: <clean | dirty：N 個檔案>
replaces: <這份取代的上一份交接路徑，沒有則 none>
---
# HANDOFF: <任務名稱>

- **目標 (Goal)**：一句話定義這件事的核心目的
- **成功指標 (Success criteria)**：怎麼判斷整件事達成
- **相關產物與狀態載體 (Related artifacts)**：<規格> ｜ <決策紀錄> ｜ <進度紀錄／任務清單> ｜ <追蹤項目>（只放路徑／連結）

## 1. WHAT：做什麼、怎麼流 (What & Flow)
- **核心邏輯 (Core logic)**：目前實作路徑或演算法（簡述，細節看 code／規格）
- **資料流向 (Data flow)**：輸入 (input) → 處理 (processing) → 輸出 (output)

## 2. WHY：決策背景 (Decision Rationale)
- **已確認 (Decided)**：<選擇>（理由；考慮過的備選 alternatives：...）
- **已排除 (Rejected)**：<方案>（放棄原因，避免重蹈覆轍）

## 3. BOUNDARY：邊界與假設 (Boundary & Assumptions)
- **範疇外 (Out of scope)**：本任務明確不處理的部分
- **規格限制 (Constraints)**：處理上限、延遲要求、資料量假設
- **環境假設 (Environment assumptions)**：第三方服務可用、資料格式永遠正確等，未經驗證的前提（標 `[unverified]`）

## 4. RISK：風險與韌性 (Risk & Robustness)
- **已知弱點 (Known weaknesses)**：哪些輸入或情境會崩潰或出錯
- **錯誤處理現況 (Error handling today)**：exception、retry、fallback 做到哪
- **變形承受力 (Scalability & changeability)**：資料量成長 10 倍或需求變更時的承受力；哪些寫死 (hard-coded)、哪些可配置 (configurable)

## 5. STATE：目前狀態與證據 (State & Evidence)
- [x] 已完成 (Done)：... `[verified]`
- [~] 開發中 (In progress)：...
- [ ] 待測試 (To be tested)：...（寫完但還沒驗證）
- [ ] 未開始 (Not started)：...
- **驗證紀錄 (Verification log)**：`<指令>` → <結果>；`[claimed]`／`[unverified]` 項目也列在這裡

## 6. CONTINUE：延續 (Continuity)
- **待解決問題 (Open questions)**：已知但尚未處理的問題
- **NEXT ACTION**：接手者的第一個具體動作（寫出指令或檔案，不要寫「繼續開發」這類空泛 (vague) 說法）
- **完成判準 (Done criteria)**：怎麼知道這一步做完了

## 7. SUGGESTED SKILLS：建議技能（沒有需要就整段省略）
- `<skill-name>`：為什麼下一步需要它、預期在哪個時機呼叫
```

## 四、接手協議 (Pickup Protocol)

每份交接都要能被這樣讀取。接手者 (receiver) 在做 NEXT ACTION 之前：

1. 確認工作目錄與分支。
2. 比對目前版本與 `base_revision`，再看未提交變更。不一致就以專案實際狀態為準，並在開工前一句話指出落差 (discrepancy)。
3. 讀交接與其連結的產物、狀態載體。
4. 重跑便宜的 `[verified]` 指令，例如基準測試 (baseline test)。結果與交接不同，就信結果。
5. 只做 NEXT ACTION，完成後依第六節更新或升級狀態。

## 五、自動模式 (`--auto`，無人在場，例如 hook 或 context 門檻自動觸發)

- **不提問、不等回覆。** 缺的資訊寫「未討論」，不要停下來問。
- **寫入範圍 (write scope)**：只寫 `handoff/`，以及專案已明定由 agent 維護的狀態載體（例如附加式進度紀錄、覆寫式現況文件）。其他載體不動，需要更新的列在 NEXT ACTION 讓接手者處理。
- 輸出會被直接貼進新對話，所以比平常更短、更自足 (self-contained)，以路徑引用取代內容；每個欄位仍然保留，內容可縮到最短。
- 回覆只包含交接本身，不加前言與結語；先存檔，再把全文輸出，供程式擷取。
- 檔案末尾附一段**接手啟動提示 (bootstrap prompt)**（3 到 5 行）：讀這份交接、依第四節驗證、再執行 NEXT ACTION。
- 靠近 context 上限時，優先保住「已排除」方案與 `[unverified]` 項目，這兩類最難從專案重建。

## 六、升級判斷與生命週期 (Promotion & Lifecycle)

交接是暫存轉運站 (transit point)。寫完前，逐項檢查內容該不該離開交接：

- 長期有效的工作規則 → 長期規則文件 (standing rules doc)
- 值得長期保留的決策與理由 → 決策紀錄 (decision log)
- 目前一段時間內有效的專案狀態 → 現況文件或進度紀錄
- 可由程式驗證的事實 → 寫成測試 (tests)
- 只對這一輪有用 → 留在交接，用完即棄

資訊越符合下列條件，越該離開對話：下一個 session 還需要、無法單靠 code／版本控制／測試推回、忘記會造成重工或風險、已被重複討論、有人負責維護、能指定唯一正本。都不符合就不用保存。

生命週期 (lifecycle)：新交接在 `replaces` 指向上一份；**只有最新一份有效**，接手者不應讀更舊的。接手並驗證完成後，把仍重要的內容升級，其餘刪除或歸檔，避免交接檔堆積成另一套知識庫。

## 七、產出前自我檢查 (Self-check)

- [ ] 已找出並沿用專案現有的狀態載體，沒有另開平行檔案？
- [ ] 目標、成功指標、第 1 至 6 塊的每個欄位都有內容或明確寫「無」「未討論」？
- [ ] 能引用的內容有沒有被複製貼上？→ 改成引用
- [ ] 殘留 API key、密碼、個資？→ `[REDACTED]`
- [ ] 每個「已完成」都有證據標籤？「寫完未驗證」有放進待測試？
- [ ] 假設接手者完全看不到上一輪聊天，只有專案本身和這份交接，下列五題答得出來嗎：現在做到哪、哪些已決定、哪些真的驗證過、還有哪些未知、第一個動作是什麼？
- [ ] NEXT ACTION 具體到可以直接執行？
- [ ] `base_revision`、`working_tree` 填了嗎？
- [ ] 長度合理？超過就升級或改成連結
- [ ] 存到正確位置，並回報絕對路徑（`--auto` 則輸出全文）？