# issue-report

把零散的問題線索整理成結構完整、可直接貼進 issue tracker 的 Markdown 問題回報。後端服務、資料管線與前端 UI 皆適用，依情境載入不同的補充欄位。

## 結構

```
issue-report/
├── SKILL.md                    # 常駐內容，約 3.3KB
├── references/
│   ├── backend-data.md         # 後端服務與資料管線的欄位與範例
│   └── frontend-ui.md          # 前端 UI 的欄位與範例
└── evals/                      # 打包時排除，不佔載入預算
    ├── evals.json              # 行為 eval（產出品質）
    ├── trigger_eval.json       # 觸發 eval（description 準確率）
    ├── files/                  # eval 用的輸入檔
    └── README.md               # 執行方式與判讀
```

只有 SKILL.md 常駐於 context，reference 依情境判斷後才載入。

## 安裝

把 `issue-report.skill` 上傳到 Claude 的 skill 設定，或將整個資料夾放進 skills 目錄。

## 設計取捨

**情境切換而非單一模板。** 「重現步驟」在前端是點擊序列，在資料管線可能根本不存在。與其寫一份通用到沒有指導性的模板，不如分成兩份 reference 按需載入。

**可重現性分三級。** 100% 可重現用 Steps to Reproduce；完全無法重現改用 Observations（時間、頻率、trace ID、共同條件）；中間地帶保留步驟並註明機率。硬編一份重現不了的步驟，只會讓接手的人多浪費一輪。

**寧可提問也不產骨架。** 七個 section 中四個以上只能填「待補」時不動筆。半數是空格的單會讓人誤以為已經回報過了。

**推測與現象嚴格分離。** 標題與 Summary 只放可觀測的現象。單與單之間的關聯屬於推測，只能放在 Summary 最後並標示未驗證。

**Severity 與 Priority 分開判斷。** 前者是技術影響，後者受成本與 workaround 影響，`Critical / Low` 是合法組合。

## 修改後的驗證

改動 SKILL.md 後跑 `evals/`，兩種 eval 覆蓋範圍不同，都要跑。詳見 `evals/README.md`。
