---
name: spec-by-example
description: 在開發前撰寫高品質的 Specification by Example 文件，協助測試開發理解情境。當使用者要寫需求規格、BDD spec、功能說明、Given-When-Then 情境、驗收條件、user story 的範例時，請使用此技能。當使用者說「幫我寫規格」、「寫 spec」、「BDD 情境」、「定義驗收條件」、「把需求轉成範例」，也應觸發此技能。
---

# Specification by Example Skill

將抽象需求轉化為「具體可執行的範例」，讓開發者、測試者、產品都能基於相同理解協作。

---

## 核心理念

**不寫抽象規格，改寫具體情境。**

| ❌ 抽象規格（避免） | ✅ 具體範例（目標） |
|---|---|
| 系統應該快速回應 | 當使用者點擊送出後，頁面在 2 秒內完成導向 |
| 使用者可以提款 | 當帳戶餘額 1000，提款 500 → 成功，餘額變 500 |
| 登入功能應該安全 | 當輸入錯誤密碼 5 次後，帳戶應被鎖定 15 分鐘 |

---

## Agent 角色扮演（Collaborative Specification）

在撰寫 spec 時，agent **必須同時扮演三種角色**，從不同維度審視需求：

### 🎯 Product Owner（PO）視角
- 業務目標是什麼？
- 哪些是核心 happy path？
- 使用者真正的意圖？

### 🛠️ Developer（Dev）視角
- 邊界條件是什麼？
- 哪些技術限制需要體現？
- 資料狀態的前置條件是什麼？

### 🔍 QA Tester 視角
- 哪些 edge cases 容易遺漏？
- 哪些 negative scenarios 需要覆蓋？
- 哪些組合情境有風險？

---

## 輸出格式

每個功能 spec 包含：

### 1. 功能標題 & 業務背景
```
功能：[功能名稱]
作為：[角色]
我想要：[目的]
以便於：[業務價值]
```

### 2. 規則摘要（Rules）
條列業務規則，是 examples 的來源依據。

### 3. Examples 表格（核心）
用表格呈現具體情境，必須覆蓋：
- Happy Path（正常流程）
- Edge Cases（邊界情況）
- Negative Scenarios（失敗情境）

### 4. Given-When-Then 格式（BDD 轉換）
每個關鍵情境寫成 Gherkin 格式：
```gherkin
Scenario: [情境名稱]
  Given [前置條件]
  When  [操作動作]
  Then  [預期結果]
  And   [額外驗證]（可選）
```

### 5. 待釐清問題（Open Questions）
列出目前不確定、需要與 PO/Dev/QA 確認的問題。

---

## 流程步驟

```
1. Discovery     → 理解業務需求，挖掘 PO 意圖
2. Specification → 轉化為具體 examples，三角色審視
3. Refinement    → 根據回饋補充 edge cases，持續精煉
```

---

## 執行指引

當使用者描述一個功能或需求，依序執行：

**Step 1｜理解需求**
- 若需求模糊，先提問釐清核心業務場景
- 識別主要角色（Actor）和業務目標

**Step 2｜以三種角色分析**
- PO 角色：確認 happy path 和業務價值
- Dev 角色：找出邊界條件與狀態前提
- QA 角色：列出 edge cases 與 negative scenarios

**Step 3｜產出 Examples 表格**
- 每個情境有明確的「條件 → 操作 → 結果」
- 至少包含 3-5 個不同情境
- 詳細規範請參考 [examples-guide.md](references/examples-guide.md)

**Step 4｜轉換 Given-When-Then**
- 從 examples 中挑選關鍵情境寫成 Gherkin
- 語言保持和使用者一致（中文/英文）

**Step 5｜列出 Open Questions**
- 所有不確定的業務規則、邊界條件都列出來
- 明確標示這是「需要確認」的問題

**Step 6｜邀請精煉**
- 結尾詢問使用者：「以上範例是否符合您的預期？有哪些情境需要補充或修正？」
- 根據回饋持續迭代（Continuous Refinement）

---

## 範例輸出

詳細的範例請參考 [examples-guide.md](references/examples-guide.md)。

---

## 注意事項

- **不要**撰寫測試程式碼或 step definitions（那是 Dev 的工作）
- **不要**討論自動化工具（Cucumber、SpecFlow 等）
- **專注**於讓人類可讀、可討論的 spec 文件
- **確保** examples 能獨立閱讀，無需額外解釋
