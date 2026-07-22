---
name: handoff
description: Compact the current conversation into a structured handoff document so a fresh agent (or the same agent in a new session) can pick up the work with full context. Use this whenever the user explicitly invokes /handoff, or asks to "write a handoff", "summarize this session for the next agent/session", "prepare a context dump before I close this", or similar — not for ordinary conversation summaries.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

# Handoff

將目前對話壓縮成一份「交接文件」（handoff doc），讓下一個 agent（或未來的自己）可以在**不重讀整段對話**的情況下，快速掌握脈絡並接續工作。

## 核心原則

1. **不要重複既有產物**：spec、plan、ADR、issue、commit、diff 等只要已經存在於檔案系統或版本控制中，就用路徑或 URL 引用，不要把內容複製貼上進 handoff doc。Handoff doc 的價值在於「連結 + 脈絡 + 理由」，不是「內容備份」。
2. **寫給沒有記憶的人看**：假設接手者完全不知道這段對話發生過什麼，只會讀這份文件。任何「我們剛剛決定…」的東西都要展開成可獨立理解的敘述。
3. **偏重「為什麼」而非「做了什麼」**：diff 和 commit log 已經記錄了做了什麼；handoff doc 該補的是動機、被否決的方案、還沒驗證的假設。
4. **主動遮蔽敏感資訊**：API key、密碼、token、個資（email、電話、內部帳號等）一律用 `[REDACTED]` 取代，不要照抄。
5. **若使用者有帶參數**（例如 `/handoff 接下來要處理 rate limiting`），以該描述為主軸調整文件的重點與「下一步」章節，其餘章節仍完整保留。

## 儲存位置

預設存在目前工作目錄下的 `handoff/` 資料夾（若不存在則建立）。若使用者有指定其他路徑，以使用者指定為準。

檔名建議包含任務簡短 slug 與時間戳（例如 `handoff-rate-limiter-20260722-1430.md`），避免覆蓋前一份。

> 若擔心 handoff doc 被誤 commit 進版本控制，可提醒使用者將 `handoff/` 加進 `.gitignore`，而不是強制改存到系統暫存目錄。

## 撰寫步驟

1. **掃描對話與既有產物**：找出目前已經存在的 spec/plan/ADR/issue/PR/commit，記下路徑或連結，稍後用引用取代複製。
2. **依八個維度萃取資訊**（見下方模板），資訊不足的維度可以留白或寫「未討論」，不要編造。
3. **依使用者傳入的參數調整重點**：若有指定下一階段任務，把「延續執行」與「建議技能」對齊該任務；若無參數，用目前對話最後的狀態推斷合理的下一步。
4. **檢查敏感資訊**：全文過一遍，把任何 key/密碼/個資替換成 `[REDACTED]`。
5. **列出建議技能（suggested skills）**：根據下一步工作內容，推測下一個 agent 應該主動呼叫哪些技能（例如涉及 docx/pptx/xlsx 產出、資料庫遷移、部署腳本等），並簡述何時該用。這是原始需求特別要求的區塊，不可省略。
6. **輸出檔案並回報路徑**：完成後把絕對路徑回報給使用者，不需要把全文再貼一次到對話裡（除非使用者要求）。

## Markdown 模板

```markdown
# AI Context Handoff: [任務名稱]

> 產生時間：[timestamp] ｜ 產生於：[專案/repo 路徑或名稱]
> 相關產物：[spec 路徑] ｜ [issue/PR 連結] ｜ [最新 commit hash]

## 0. 任務摘要 (What & Flow)
- **目標**：一句話定義此任務核心目的
- **成功指標**：如何判斷任務已達成
- **核心邏輯**：目前實作路徑 / 演算法邏輯（簡述，細節看 code/spec）
- **資料流向**：輸入（Input）→ 處理 → 輸出（Output）

## 1. 決策背景 (Why)
- **技術選型原因**：為什麼選現在這個方案，而非其他備選
- **已排除方案**：試過但放棄的方法，以及放棄原因（避免重蹈覆轍）

## 2. 邊界與假設 (Boundary & Assumption)
- **範疇外事項**：明確列出「本任務不處理」的部分
- **效能/規格限制**：處理上限、延遲要求、資料量假設等
- **環境假設**：假設第三方服務可用、假設資料格式永遠正確等未經驗證的前提

## 3. 風險與壓力測試 (Failure & Robustness)
- **已知弱點**：哪些輸入 / 情境會導致崩潰或邏輯錯誤
- **錯誤處理現況**：目前的 exception handling / retry / fallback 機制
- **抗變形能力**：若資料量成長 10 倍、或需求變更，現有架構的承受力
- **模組化程度**：哪些寫死（hard-coded），哪些可配置

## 4. 延續執行 (Continuity)
- **目前狀態**：已完成 / 開發中 / 待測試（用 checklist 呈現）
- **待解決問題**：已知但尚未處理的 open questions
- **下一步指令建議**：接手者應執行的第一個具體動作（越具體越好，避免「繼續開發」這種空泛描述）

## 5. 建議技能 (Suggested Skills)
- `<skill-name>`：為什麼下一步需要它、預期在哪個時機呼叫
```

## 品質檢查（產出前自我檢查）

- [ ] 有沒有把本來可以用路徑/連結引用的內容，錯手複製貼上進來？→ 改成引用
- [ ] 有沒有殘留 API key、密碼、個資？→ 替換為 `[REDACTED]`
- [ ] 「下一步指令建議」是否具體到可以直接執行，而不是空泛的方向？
- [ ] 是否有「建議技能」區塊，且每個技能都說明了觸發時機？
- [ ] 檔案是否存到正確的位置（預設 `handoff/`，或使用者指定的路徑）？