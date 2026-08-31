# Examples Guide

SKILL.md 講規則，這份講「長怎樣」。三個部分：

1. [Edge／Fail 檢查清單](#1-edgefail-檢查清單) — 三角色審視時逐項掃過，補齊 E 與 F 案例
2. [格式選項](#2-格式選項) — Examples 表格太寬、只有一組值、多維組合時怎麼排
3. [完整範例：訂單建立 API 的冪等保證](#3-完整範例訂單建立-api-的冪等保證) — 從功能背景到 Open Questions 全區塊填滿

---

## 1. Edge／Fail 檢查清單

寫完 Normal 之後逐項掃。不是每項都要有案例，但每項都要問過一次；問過覺得不適用，比沒想到好。

### 數值與量值

- 剛好等於上限／下限；上限 +1、下限 −1
- 0、負數、空值（null 與「沒帶這個欄位」是兩件事）
- 極大值：溢位、超過欄位長度、超過下游 payload 上限
- 小數精度、四捨五入方向、貨幣最小單位

### 集合與順序

- 空集合、只有一筆、剛好等於分頁上限、超過分頁上限
- 重複元素、順序顛倒、部分成功（批次裡有一筆壞的）
- 未知的列舉值（上游新增了一個你沒處理的 enum）

### 時間

- 剛好到期 vs 剛好還沒到期
- 時區、日界線、DST 轉換當天
- 時鐘回跳、事件亂序抵達、遲到的事件（late arrival）

### 併發與重試

- 兩個請求同時打同一筆資源
- 網路逾時後重送（呼叫方不知道第一次成不成功）
- 前一次跑到一半失敗後重跑

### 權限與狀態

- 無權限、權限剛好足夠、權限中途被撤銷
- 狀態機不允許的轉移（已取消的訂單再取消）
- 資源不存在、已刪除、已封存

### 外部依賴

- 逾時、5xx、回傳格式不符預期
- 依賴降級時的預期行為（擋下來？放行？記帳後補？）
- 依賴回覆得比預期慢，但最後成功了

### 資料品質

- 欄位缺漏、型別錯誤、超長字串
- 編碼、全形半形、前後空白
- 同一份資料的兩個來源互相矛盾

---

## 2. 格式選項

**預設**：一條規則一張 Examples 表，欄名 = GWT 的 placeholder。

**placeholder 超過 6 個**：表格會寬到要橫捲。多半代表這條規則管太多事——先試著拆成兩條規則。真的拆不開（例如一次分類要看四個訊號），把不變的前置條件收進 GWT 的固定文字，只讓真正變動的維度上表格。

**只有一組值**：不要為了格式硬開表格。直接把值寫進 GWT：

```gherkin
Given 帳戶已被鎖定
When  持卡人提款 100
Then  交易被拒絕，理由為「帳戶鎖定」
```

**多維組合**：兩個維度各三種值 = 九種組合，但通常只有四五種有意義。列出有意義的那幾筆，並在規則裡寫清楚沒列的為什麼不用測（等價類別、或由另一條規則覆蓋）。不要為了填滿矩陣而生案例。

**同一筆資料被多條規則用到**：直接引用 ID，不要複製一份。「沿用 FR-1.N1 的帳戶狀態」比重打一次表格好——重打的那份遲早會跟本尊不一致。

---

## 3. 完整範例：訂單建立 API 的冪等保證

以下是一份填好的 spec，示範所有區塊怎麼一起運作。

---

# 訂單建立 API 的冪等保證

## 功能背景

- **功能**：`POST /v1/orders` 的冪等（idempotency）保證
- **作為** 串接下單 API 的呼叫方
- **我想要** 在網路逾時後安全重送同一筆請求
- **以便於** 不會因為重試而建出兩張訂單

## Problem Statement

呼叫方送出下單請求後遇到連線逾時，此時無法判斷訂單是否已經建立。目前的行為是重送就會多一張訂單，呼叫方只能選擇「不重試但可能漏單」或「重試但可能重複」。實務上兩種都發生過，重複下單需要人工對帳沖銷。

## Solution

呼叫方在 header 帶 `Idempotency-Key`。同一把 key 在有效期內只會產生一次副作用；重送時直接回放第一次的回應，讓「重試」變成安全操作。

## User Stories

- **US-Client-1**：作為呼叫方，我想要重送同一筆請求時不會產生第二張訂單，以便於逾時後可以直接重試
- **US-Client-2**：作為呼叫方，我想要重送時拿到與第一次完全相同的回應，以便於不必為重試寫特別的處理分支
- **US-Client-3**：作為呼叫方，我想要用同一把 key 送不同內容時被明確擋下，以便於及早發現自己 key 產生邏輯的 bug
- **US-Client-4**：作為呼叫方，我想要知道 key 的有效期限，以便於決定重試視窗要開多長
- **US-Operator-1**：作為維運，我想要併發重送不會建出兩張訂單，以便於不必人工對帳
- **US-Operator-2**：作為維運，我想要冪等記錄有保存上限，以便於儲存成本可控
- **US-Operator-3**：作為維運，我想要冪等層故障時的行為是可預期的，以便於決定要不要降級放行

## 業務規則與情境

### FR-1｜Idempotency-Key 為必填且需符合格式

**Story**：

- US-Client-1（安全重試）
- US-Client-3（及早發現 key 產生 bug）

**Rule**：`Idempotency-Key` header 缺漏或格式不符時，整筆請求拒絕，不建立訂單。格式為 16–128 個字元的 `[A-Za-z0-9_-]`。

**Given-When-Then**

```gherkin
Given 呼叫方帶的 Idempotency-Key 為 <idempotency_key>
When  送出一筆合法的下單請求
Then  回應狀態碼為 <status>
And   訂單建立筆數為 <orders_created>
```

**Examples**

| ID | idempotency_key | status | orders_created |
|---|---|---|---|
| FR-1.N1 | `a3f9c1e2-4b7d-8a01` (18 字元) | 201 | 1 |
| FR-1.E1 | 16 個合法字元 | 201 | 1 |
| FR-1.E2 | 128 個合法字元 | 201 | 1 |
| FR-1.E3 | 129 個合法字元 | 400 | 0 |
| FR-1.F1 | header 未帶 | 400 | 0 |
| FR-1.F2 | 空字串 | 400 | 0 |
| FR-1.F3 | 含空白與 `/` | 400 | 0 |

### FR-2｜同 key 同內容重送回放原回應

**Story**：

- US-Client-1（安全重試）
- US-Client-2（回應一致）

**Rule**：同一把 key 在有效期內、且請求主體的正規化雜湊相同時，不再執行下單，直接回放第一次的狀態碼與主體，並帶 `Idempotency-Replayed: true`。

**Given-When-Then**

```gherkin
Given 已用 key K 成功建立訂單，回應為 201 與 order_id O
When  以相同的 key K 與 <body_change> 再送一次
Then  回應狀態碼為 <status>
And   回應的 order_id 為 <returned_order_id>
And   訂單總筆數為 <total_orders>
```

**Examples**

| ID | body_change | status | returned_order_id | total_orders |
|---|---|---|---|---|
| FR-2.N1 | 完全相同的主體 | 201 | O | 1 |
| FR-2.E1 | 欄位順序不同、值相同 | 201 | O | 1 |
| FR-2.E2 | 多／少無意義空白 | 201 | O | 1 |
| FR-2.E3 | 第一次的結果是 400（業務驗證失敗） | 400 | 無 | 0 |

第一次若是 5xx，該 key 不留紀錄，重送視為新請求——見 Open Questions Q2。

### FR-3｜同 key 不同內容一律拒絕

**Story**：

- US-Client-3（及早發現 key 產生 bug）

**Rule**：同一把 key 搭配不同的請求主體雜湊時，回 422 並附上衝突說明，不建立訂單、不覆寫既有紀錄。

**Given-When-Then**

```gherkin
Given 已用 key K 成功建立訂單 O
When  以相同的 key K 送出 <changed_field> 不同的請求
Then  回應狀態碼為 <status>
And   訂單總筆數為 <total_orders>
```

**Examples**

| ID | changed_field | status | total_orders |
|---|---|---|---|
| FR-3.N1 | `amount` 由 100 改為 200 | 422 | 1 |
| FR-3.E1 | 只有 `note` 這種不影響金流的欄位不同 | 422 | 1 |
| FR-3.F1 | 主體完全空白 | 422 | 1 |

FR-3.E1 刻意不做「無關欄位可放行」的例外：判斷哪些欄位無關會隨業務變動，一旦開例外就得維護一份白名單。代價是呼叫方改 note 重送會被擋，需在文件寫明。

### FR-4｜併發重送只成功一筆

**Story**：

- US-Client-1（安全重試）
- US-Operator-1（不必人工對帳）

**Rule**：同一把 key 的多個請求同時進來時，僅一個進入建立流程；其餘等待其完成後回放結果。等待超過 5 秒則回 409，呼叫方可稍後重試。

**Given-When-Then**

```gherkin
Given 沒有任何 key K 的既有紀錄
When  <concurrent_count> 個帶 key K 的相同請求在 <arrival_window> 內同時抵達
Then  回 201 的筆數為 <count_201>
And   訂單總筆數為 <total_orders>
```

**Examples**

| ID | concurrent_count | arrival_window | count_201 | total_orders |
|---|---|---|---|---|
| FR-4.N1 | 2 | 10ms | 2（一筆為回放） | 1 |
| FR-4.E1 | 50 | 10ms | 50 | 1 |
| FR-4.F1 | 2，且首筆處理耗時 6 秒 | 10ms | 1 | 1 |

FR-4.F1 的第二筆回 409。

### FR-5｜key 有效期為 24 小時

**Story**：

- US-Client-4（決定重試視窗）
- US-Operator-2（儲存成本可控）

**Rule**：冪等紀錄自建立起保存 24 小時，逾期刪除。逾期後同一把 key 視為全新請求，會建立新訂單。

**Given-When-Then**

```gherkin
Given 已用 key K 於 T0 成功建立訂單
When  於 <elapsed> 後以相同的 key K 與相同主體重送
Then  回應狀態碼為 <status>
And   訂單總筆數為 <total_orders>
```

**Examples**

| ID | elapsed | status | total_orders |
|---|---|---|---|
| FR-5.N1 | 1 小時 | 201（回放） | 1 |
| FR-5.E1 | 23 小時 59 分 | 201（回放） | 1 |
| FR-5.E2 | 24 小時 01 分 | 201（新建） | 2 |
| FR-5.F1 | 1 小時，但紀錄已被維運手動清除 | 201（新建） | 2 |

### FR-6｜冪等層故障時的降級行為

**Story**：

- US-Operator-3（故障時行為可預期）

**Rule**：冪等儲存不可用時，下單一律回 503 並附 `Retry-After`，不放行。寧可拒單，也不接受靜默失去冪等保證。

**Given-When-Then**

```gherkin
Given 冪等儲存處於 <storage_state>
When  送出一筆帶合法 key 的下單請求
Then  回應狀態碼為 <status>
And   訂單建立筆數為 <orders_created>
```

**Examples**

| ID | storage_state | status | orders_created |
|---|---|---|---|
| FR-6.N1 | 正常 | 201 | 1 |
| FR-6.E1 | 讀取正常、寫入失敗 | 503 | 0 |
| FR-6.F1 | 完全不可用 | 503 | 0 |
### NFR-1｜冪等檢查不得成為下單瓶頸

**Story**：

- US-Client-1（安全重試不能換來變慢）

**Rule**：冪等檢查（含查詢與寫入）在 `POST /v1/orders` 的 p99 額外延遲不超過 15ms。超過視為違反，需告警。

**Given-When-Then**

```gherkin
Given 冪等儲存處於 <storage_state>
When  以 200 RPS 持續送出下單請求 5 分鐘
Then  冪等檢查的額外延遲 p99 為 <p99_added_latency>
```

**Examples**

| ID | storage_state | p99_added_latency |
|---|---|---|
| NFR-1.N1 | 正常，紀錄數 10 萬筆 | ≤ 15ms |
| NFR-1.E1 | 正常，紀錄數 1000 萬筆（保存上限） | ≤ 15ms |
| NFR-1.F1 | 儲存回應延遲 500ms | 觸發降級，見 FR-6 |


## Implementation Decisions

- 冪等判定放在 HTTP handler 與 use-case 之間的 middleware，use-case 本身不知道冪等的存在。理由：讓其他寫入端點日後能沿用同一層。
- 儲存採「先寫入 key 佔位（狀態 `in_flight`）→ 執行 → 回寫結果」兩段式，靠儲存層的唯一鍵約束處理併發，不另外加分散式鎖。
- 請求主體雜湊採正規化後的 SHA-256：JSON 鍵排序、移除無意義空白，不做欄位過濾（呼應 FR-3.E1）。
- 回放的回應逐位元組保存，包含當時的狀態碼與 `Content-Type`；不重新序列化，避免版本升級後回放內容跟第一次不同。
- 新增三個回應 header：`Idempotency-Replayed`、`Idempotency-Expires`、以及 409／503 時的 `Retry-After`。

## Testing Decisions

接縫選項：

| 選項 | 接縫位置 | 能驗到的 Examples | 驗不到的 | 測試成本 |
|---|---|---|---|---|
| A | `POST /v1/orders` handler，`httptest` + 真實儲存實例，下游支付以 fake 取代 | 全部 | — | CI 每次多約 8 秒（啟動 container） |
| B | 同 A，但儲存以 mock 取代 | FR-1、FR-2、FR-3、FR-6 | FR-4 併發、FR-5 過期 | 每次 < 1 秒 |
| C | 直接測冪等 middleware 的函式 | FR-1、FR-3 | FR-2 的回放位元組一致、FR-4、FR-5、FR-6 | 每次 < 1 秒 |

**建議 A。** 冪等的正確性高度依賴儲存層的唯一鍵語意，B 用 mock 取代儲存等於把要驗的東西驗掉了——FR-4 一整條就是在驗那個語意。C 連 HTTP 層的回放行為都碰不到。8 秒的啟動成本相對於「併發重複下單」這個要修的問題，可以接受。

若 8 秒不能接受，退 B，並把「FR-4、FR-5 只在 staging 手動驗證」寫成已知缺口——但這兩條正是這次要修的問題，退之前先想清楚。

- FR-4 的併發案例以同一個測試內開多個 goroutine 對 handler 發請求，斷言最終訂單筆數而非執行順序。
- NFR-1 不進 CI，走每晚的負載測試流程，門檻寫進既有的 latency budget 設定檔。
- Prior art：`internal/api/payment_callback_test.go` 已有「重複回呼只處理一次」的類似測試，沿用它的 fixture 與 container 啟動輔助函式。

## Out of Scope

- 其他寫入端點（取消、改單）的冪等——本次只做建立。
- 呼叫方端的 key 產生策略與 SDK 支援。
- 跨區域的冪等紀錄同步：本次僅保證單一區域內。

## Open Questions

| # | 問題 | 類型 | 負責人 |
|---|---|---|---|
| Q1 | FR-3 回 422 或 409？現有錯誤碼慣例偏好哪一個 | Dev | 後端 |
| Q2 | 第一次回 5xx 時，key 應留紀錄（讓重送回放 5xx）或不留（視為新請求）？目前暫定不留 | PO | 產品 |
| Q3 | 24 小時是否足夠涵蓋合作夥伴最長的重試視窗？需要跟前三大呼叫方確認 | PO | 產品 |
| Q4 | FR-4 的 5 秒等待上限，與呼叫方端的 timeout 設定是否衝突 | Dev | 後端 |
| Q5 | FR-6 的「一律拒單」是否需要為特定高優先呼叫方開例外 | PO | 產品 |

## Further Notes

- 冪等紀錄的清除採 TTL 自動過期，不寫排程；FR-5.F1 的手動清除情境僅描述行為，不是支援的操作。
- `Idempotency-Key` 的 header 名稱沿用 IETF 草案的寫法，未來若標準定案可平滑對齊。
