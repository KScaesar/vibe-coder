---
name: issue-report
description: 把零散的問題線索整理成結構完整、可直接貼上 issue tracker 的 Markdown 問題回報，含標題、Summary、Environment、重現步驟或觀測證據、Impact、Severity/Priority。使用者說「幫我寫個 issue」「回報這個 bug」「開個 ticket」，或丟出 log、stack trace、告警、對話紀錄並要轉成正式回報時使用；即使沒說出「issue」兩個字，只要意圖是把異常交給別人接手處理就適用。後端服務、資料管線（pipeline/job/table）與前端 UI 皆適用，依情境切換欄位。不適用於：只想除錯或找 root cause、事後的 postmortem／RCA、PR 說明與 release note、功能需求單。
---

# Issue Report

把零散的線索整理成別人不用追問就能開始查的 issue。

輸出純 Markdown，不綁定任何 issue tracker。敘述用繁體中文；識別名、欄位名、錯誤訊息、技術術語（`timeout`、`partition`、`stack trace`）一律保留英文原文，標題同此規則。

## 設計取捨

**情境切換而非單一模板。** 「重現步驟」在前端是點擊序列，在資料管線可能根本不存在。與其寫一份通用到沒有指導性的模板，不如分成兩份 reference 按需載入。

**可重現性分三級。** 100% 可重現用 Steps to Reproduce；完全無法重現改用 Observations（時間、頻率、trace ID、共同條件）；中間地帶保留步驟並註明機率。硬編一份重現不了的步驟，只會讓接手的人多浪費一輪。

**寧可提問也不產骨架。** 七個 section 中四個以上只能填「待補」時不動筆。半數是空格的單會讓人誤以為已經回報過了。

**推測與現象嚴格分離。** 標題與 Summary 只放可觀測的現象。單與單之間的關聯屬於推測，只能放在 Summary 最後並標示未驗證。

**Severity 與 Priority 分開判斷。** 前者是技術影響，後者受成本與 workaround 影響，`Critical / Low` 是合法組合。

## 先判斷情境

「重現步驟」在不同情境下意義完全不同，所以先定位再動筆：

| 情境 | 判斷線索 | 補充欄位 |
|---|---|---|
| 後端服務 / API | endpoint、status code、latency、service 名稱、deployment | `references/backend-data.md` |
| 資料管線 / 資料正確性 | table、partition、job、DAG、筆數對不上、schema | `references/backend-data.md` |
| 前端 / UI | 瀏覽器、按鈕、頁面、樣式、裝置 | `references/frontend-ui.md` |

兩類線索都有就兩份都讀。完全判斷不出來時，用下方通用模板寫，並把情境本身列為待補項（見「資訊不足時」）。

## 標準模板

除非使用者另有指定，一律用這個結構：

```markdown
# <標題>

## Summary
<2~4 句。同樣回答什麼／哪裡／何時，但填入精確值，再加上為什麼需要處理、影響誰。>

## Environment
- <依情境列出必要欄位>

## Steps to Reproduce
1. <步驟>
2. <步驟>

## Expected vs Actual
- **Expected**：<應該發生什麼>
- **Actual**：<實際發生什麼>

## Impact
<受影響的使用者或流量比例、資料範圍、是否有 workaround。>

## Evidence
<log、error message、query、截圖說明。長 log 只留關鍵段落。>

## Severity / Priority
- **Severity**：Critical / Major / Minor / Trivial — <一句理由>
- **Priority**：High / Medium / Low — <一句理由>
```

## 什麼 what ／哪裡 where ／何時 when

標題與 Summary 回答同樣三個問題，差別只在精度。任一軸缺漏，讀的人就得回頭追問。

| | 什麼 | 哪裡 | 何時／什麼條件 |
|---|---|---|---|
| 標題 | 可觀測的現象，一句話 | 可辨識的最短範圍 | 觸發條件 |
| Summary | 現象的量化描述：數值、錯誤碼、與基準的差異 | 完整識別名：full table name、endpoint、build number | 具體時間區間含時區、首次出現時間、頻率 |

Summary 另外要交代標題塞不下的兩件事：**為什麼這是問題**、**影響誰**。不要把標題換句話說就當 Summary——沒有新增精度等於沒寫。

兩者都只描述可觀測的現象，不寫推測出來的成因，寫成因會讓後續調查預設立場。

標題：
- ✅ `Checkout API 在購物車超過 50 項時回傳 504`
- ✅ `daily_ad_impression partition 2026-09-21 缺少 lg_channels 來源資料`
- ❌ `Redis 掛了`（推測，不是現象）
- ❌ `結帳壞掉`（沒有哪裡、沒有條件）

Summary：
- ✅ `2026-09-22 03:00 CST 的 ad-impression-daily run 對 partition 2026-09-21 寫入 0 筆 lg_channels 資料（前七天平均 1.2M），job 仍回報 SUCCESS。該表為每日對帳上游，09-22 報表已低估。`
- ❌ `lg_channels 的資料好像有問題，麻煩查一下。`（三軸皆缺，也沒說影響）

## 無法穩定重現時

偶發問題（race condition、特定流量才觸發、上游髒值）沒有可靠步驟。硬編一份出來，對方照做重現不了只會多一輪來回。此時刪掉 `Steps to Reproduce`，換成：

```markdown
## Observations
- **發生時間**：<時間區間，含時區>
- **發生頻率**：<24 小時內 3 次 / 約 0.2% 請求>
- **定位線索**：<trace ID、request ID、job run ID、受影響的 key 或 partition>
- **共同條件**：<例如只在尖峰時段、只在特定 tenant>
```

時間與頻率在 Summary 只給一句話版本，精確值放這裡，不要兩邊重複貼。

能穩定重現但機率不是 100% 時，保留 `Steps to Reproduce` 並在最後一行註明重現機率。

## 資訊不足時

不要為了填滿欄位而捏造內容——假的版本號或步驟會把人帶去查錯方向，比空白更糟。

**動筆前先數一次**：模板七個 section 中，若有四個以上只能填「待補」，不要產出骨架——一張半數是空格的單，對接手的人沒有價值，還會讓人誤以為已經回報過了。改成先問 2–3 個最關鍵的問題，拿到答案再寫。

優先問能解鎖最多欄位的問題：發生時間與頻率、精確的位置（service／table／頁面與環境）、以及是否每次都發生。

其餘情況用已知資訊先寫完，缺的欄位標成 `待補：<具體要哪一筆資料>`（例如「待補：出問題時的 service version 與 trace ID」，不是「待補：環境資訊」）。回覆末尾再列出最關鍵的 2–3 個待補項。

## Severity 與 Priority 分開判斷

- **Severity**＝技術影響多嚴重。資料靜默錯誤即使沒人抱怨也可能是 Critical。
- **Priority**＝多快要修。受成本、時程、有無 workaround 影響。

所以 `Severity: Critical / Priority: Low` 是合法組合（例如已停用的 legacy 服務嚴重損壞）。兩者都附一句理由，讓對方能反駁。

## 一張單一個問題

使用者一次講多個現象時，先判斷是不是同一個 root cause 的不同表徵：

- 同源 → 一張單，其他現象放進 Evidence 當佐證。
- 獨立 → 拆成多張，各自完整，在 Summary 互相 cross-reference。

判斷不確定就照拆的方向做，並說明拆法依據。

單與單之間的關聯屬於推測，不能寫進標題或 Summary 的現象描述。要提就放在 Summary 最後獨立一行，明確標成未驗證：`疑似與 <另一張單> 相關，尚未驗證。`

## 輸出

寫成 `.md` 檔案供下載，不要只在對話中輸出。

- 檔名用標題的短 slug：`issue-checkout-submit-no-response.md`、`issue-daily-ad-impression-missing-partition.md`
- 拆成多張單時一張一個檔，不要併在同一個檔裡
- 回覆本身只寫需要使用者決策的部分：拆單依據、待補項、Severity/Priority 的判斷理由。不要把整張單的內容再貼一次

資訊不足而改成提問時，不產生檔案。使用者明確說要直接貼在對話裡時，依其指示。
