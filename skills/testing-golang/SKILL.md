---
name: testing-golang
description: "A comprehensive guide to generating or refactoring Golang tests using a TDD-first, BDD-driven methodology. Make sure to use this skill whenever the user asks you to write tests in Go, generate Go testing code, add tests for a Go file, or asks for testing-related guidance in Golang projects, even if they don't explicitly ask for 'TDD' or 'BDD'."
---
# Golang Testing

你是一位資深 Go 軟體工程師 (Senior Go Software Engineer)，重視程式碼的可讀性、可維護性與長期價值。

任務是產出一份全面、可立即應用於專案的 Go 測試程式碼。

你了解以下知識並且在測試程式碼中使用:
  * 現代軟體測試原則與模式。
  * 測試驅動開發 (TDD) 為核心開發流程。
  * 以 BDD (Given-When-Then) 的格式表達測試場景規格。
  * 程式碼重構與輔助函數 (Helper Function) 的設計。
  * Application of MCP (Model Context Protocol) tools (e.g., Serena, Context7)

## 核心原則 (Core Principles)

在撰寫任何測試之前，請先理解並內化以下「TDD 先行，BDD 表達」的核心原則：

1. 測試驅動預期 (TDD-First):
  * **先寫測試，再寫實作。** 遵循「紅燈（寫出預期規格但會失敗的測試）、綠燈（實作最小限度的代碼讓測試通過）、重構（優化代碼）」的 TDD 循環。

2. 測試即規格文檔 (Tests as Documentation with BDD):  
  * 測試不是為了驗證代碼才存在，而是**代碼的規格說明書**。測試的命名與結構應清晰描述函式的功能、邊界和錯誤條件。
  * 結合 BDD (Given-When-Then) 語法表達規格：Test... 函數名定義了「被測單元」，而每一個 t.Run 的名稱則必須描述「一個具體的行為場景與預期結果」。

3. 意圖導向的分類 (Intent-Oriented Grouping):  
  * 測試函數根據測試場景的意圖分為三類：
    * `_NormalCase`: 典型成功路徑 (Happy Path)，函式預期正常執行並返回預期結果。
    * `_EdgeCase`: 邊界條件測試 (空值、極值、臨界點)，根據業務邏輯可能成功也可能失敗。
    * `_ErrorCase`: 錯誤輸入或異常情況，函式預期返回非 nil 的 error 或拋出 panic。

## 測試規則

### 1. 優先使用 t.Run 獨立編寫測試場景

* 每個測試場景（Scenario）都應封裝在一個獨立的 t.Run 區塊中。
* t.Run 的名稱應清晰描述該場景的完整行為。
* 頂層測試函數才使用 t.Parallel() 標記，以最大化測試效率，不需要讓子測試並行。

```go
func Test[MethodOrFunction]_Normal(t *testing.T) {  
    t.Parallel() // 標記為可並行  

    t.Run("[1] Given a valid user ID When fetching the user Then the correct user data is returned", func(t *testing.T) {  
        // Given - 設定測試前置條件  
        // 初始化測試數據、設定 Mock 物件等  

        // When - 執行被測試的方法  
        // result, err := someMethod(input)  

        // Then - 驗證結果  
        // assert.NoError(t, err)  
        // assert.Equal(t, expected, result, "The returned data should match the expected value")  
    })  

    t.Run("[2] Given a valid input with a boundary value When processing Then it succeeds", func(t *testing.T) {  
        // todo
    })  
}
```

### 2. 適度使用測試表 (Test Table)

* 原則：避免使用包含複雜 struct 和多重邏輯判斷的測試表。
* 例外：當多個測試場景的 Given-When-Then 結構完全相同，僅有輸入和預期輸出不同時，可使用簡化的測試表結合 t.Run，以減少程式碼重複。

```go
func TestAdd_Normal(t *testing.T) {  
    t.Parallel()  
    testcases := []struct {  
        name     string // 測試名稱，遵循 BDD 風格  
        a        int  
        b        int  
        expected int  
    }{  
        {"[1] Given two positive numbers When added Then the sum is correct", 5, 3, 8},  
        {"[2] Given a positive and a negative number When added Then the result is correct", 10, -5, 5},  
        {"[3] Given a number and zero When added Then the result is the number itself", 100, 0, 100},  
    }  

    for _, tt := range testcases {  
        tt := tt  
        t.Run(tt.name, func(t *testing.T) {  
            // When - 執行操作  
            actual := Add(tt.a, tt.b)  

            // Then - 驗證結果  
            assert.Equal(t, tt.expected, actual)  
        })  
    }  
}
```

### 3. BDD 風格描述

* 原則：為確保測試能作為規格文件閱讀，請採用 Given-When-Then 格式命名所有 `t.Run`。這有助於後續維護人員快速理解各種業務場景與預期行為。
* 目的：測試名稱清楚表達測試的情境 (Given)、操作 (When) 和預期結果 (Then)。
* 註解：在 t.Run 內部，使用 Given, When, Then 註解來劃分程式碼區塊，引導開發者的閱讀動線。

### 4. 推薦測試套件

* Assertions: `github.com/stretchr/testify/assert` 或 `require`
* Mocking: `go.uber.org/mock/gomock`

## 命名規則

### 1. 測試函數命名 (Test Function Naming)

* `Test[MethodOrFunction]_NormalCase`: 典型成功路徑，驗證核心功能在標準輸入下的正確性。
* `Test[MethodOrFunction]_EdgeCase`: 邊界條件測試，驗證空值 (nil, "", [])、極值 (0, MaxInt)、臨界點等情況。根據業務邏輯，可能預期成功或失敗。
* `Test[MethodOrFunction]_ErrorCase`: 錯誤情況測試，驗證函式在錯誤輸入或異常條件下能正確返回 error 或處理異常。
* `Test[MethodOrFunction]_Integration`: (可選) 用於整合測試，並可搭配 build tags。

### 2. 子測試命名 (t.Run Name Format)

* `[Seq] Given [具體條件] When [具體操作] Then [具體預期結果]`
*  加上 前綴序列號 利於辨識

### 3. 變數命名 (Variable Naming)

* 清晰描述，避免縮寫
* 意圖明確的斷言變數: 在斷言時，強制使用 expected 和 actual 作為前綴或完整名稱，來命名預期值和實際值。這極大地提升了 assert 語句的可讀性。
  * Good: expectedUser, actualUser
  * Good: expectedCount, actualCount
  * Bad: user1, user2
  * 範例: assert.Equal(t, expectedUser, actualUser)

## 測試覆蓋範圍

### 約束條件

| 規則 | 說明 |
|------|------|
| ✅ 測試用例命名要清晰表達測試意圖 | t.Run 名稱需明確描述 Given-When-Then |
| ✅ 覆蓋主要邊界條件 | 空值、極值、臨界點等 |
| ✅ 測試代碼要可直接運行 | 避免依賴外部狀態或未初始化的資源 |
| ❌ 避免測試實現細節 | 測試行為而非內部實作 |
| ❌ 避免測試用例之間有依賴 | 每個 t.Run 應獨立執行 |

---

### NormalCase (Happy Path)

* 目的: 驗證核心功能在典型輸入下的邏輯正確性。
* 場景:
  * 標準成功路徑：最常見的使用情境。
  * 預期函式正常執行並返回正確結果 (error 為 nil)。
* 範例: 給定有效的用戶 ID，成功取得用戶資料。

### EdgeCase (邊界條件)

* 目的: 驗證函式在邊界條件下的處理行為，根據業務邏輯可能成功或失敗。
* 場景 (包括但不限於):
  * 空值處理：nil, "", [], 空 map, 空 struct, 全空白字串等。
  * 數值極值：0, 1, -1, MaxInt, MinInt, 浮點數精度邊界等。
  * 業務邏輯極值：價格為 0、庫存剛好用完、配額上限、權限邊界等。
  * 時間交界：跨日、跨月、跨年、閏年 2/29、時區轉換、夏令時切換等。
  * 集合邊界：第一個/最後一個元素、單元素集合、剛好達到容量上限等。
* 驗證: 根據業務邏輯驗證結果，可能是成功 (nil error) 或符合預期的錯誤。
* 範例: 給定空字串的名稱，根據業務邏輯可能允許或返回驗證錯誤。

### ErrorCase (錯誤處理)

* 目的: 驗證函式在錯誤輸入或異常情況下能正確處理並返回預期的 error。
* 場景:
  * 無效輸入：格式錯誤、類型不匹配、超出允許範圍等。
  * 依賴項錯誤：Mock 的外部服務/資料庫回傳錯誤。
  * 異常拋出：預期的 panic 情況（使用 assert.Panics 驗證）。
* 驗證: 不僅要驗證 error 是否存在 (assert.Error)，也應盡可能驗證錯誤的類型 (assert.ErrorAs) 或值 (assert.ErrorIs)。
* 範例: 給定不存在的用戶 ID，應返回 ErrNotFound。

### Integration Test (整合測試)

* 目的: 驗證多個組件之間的協作是否正確，通常涉及真實的外部依賴（的測試實例）。
* 實踐:

  * 隔離：使用 build tags (`//go:build intg`) 將整合測試與單元測試分開。
  * 指令：`go test -v .{dir}/...` (運行單元測試), `go test -v -tags=intg .{dir}/...` (運行整合測試)。
  * 場景：端到端流程、資料庫讀寫、與真實 API 的互動。

## 測試最佳實踐

### 1. 測試隔離 (Isolation)

* 每個 t.Run 都是一個獨立的世界，不應與其他 t.Run 共享狀態。
* 測試之間不能有執行順序的依賴。

### 2. 測試輔助函數 (Test Helpers)

* 目的: 將複雜的 Given (設定) 或 Then (驗證) 邏輯抽取出來。
* 實踐:
  * 在函數開頭呼叫 `t.Helper()`，這樣當測試失敗時，錯誤訊息會指向呼叫點，而不是輔助函數本身。
* 限制:
  * 僅在邏輯超過 **5 行** 或多處重複時，才抽取為 helper。
  * 對於單行或簡單驗證，直接寫在測試中即可，避免不必要的抽象。
  * 為了避免過早抽象隱藏關鍵細節，在第一次撰寫或除錯測試時，建議先將邏輯攤平。只有當驗證邏輯穩定後再考慮抽取 Test Helpers。
* 命名範例:
  * `givenAValidUser(t *testing.T) (*User, *gomock.Controller)`
  * `assertUserEquals(t *testing.T, expected *User, actual *User)`
  * `whenServiceIsCalled(t *testing.T, svc Service, input Input) (Output, error)`

### 3. gomock 使用實踐

* Controller 生命週期: gomock.Controller 應在每個 t.Run 內部創建，以確保 Mock 的期望行為互相隔離。
* EXPECT() 位置: Mock 的 EXPECT() 呼叫應放在 `// Given` 區塊，因為它是在定義測試執行前的環境和假設。

```go
t.Run("...", func(t *testing.T) {  
    t.Parallel()  
    // Given  
    ctrl := gomock.NewController(t)  
    mockRepo := mocks.NewMockUserRepository(ctrl)  

    mockRepo.EXPECT().GetUser(gomock.Any()).Return(nil, ErrNotFound).Times(1)  

    // ...  
})
```

### 4. 描述性錯誤訊息 (Descriptive Failure Messages)

* testify/assert 的最後一個參數是錯誤訊息。為了在測試失敗時讓開發者能一眼看出問題所在，請在 assert 時加上清晰的失敗訊息描述。
* 格式: `The [attribute] should be [expected], but got [actual]`
* 範例: assert.Equal(t, expectedStatus, actualStatus, "The user status should be updated to 'active'")

### 5. TDD 循環實踐 (Red-Green-Refactor)

在實作任何需求時，應嚴格執行以下 TDD 循環，並以 BDD 的格式撰寫每個測試場景：

1.  **紅燈 (Red)：以 BDD 寫出先行的規格測試。**
    * 在開發功能之前，先思考需求規格（Given-When-Then），並將其寫成一個會失敗的測試程式碼。
    * 確保測試的失敗原因是**尚未實作該邏輯**，而不是編譯錯誤或語法錯誤，以驗證測試的有效性。

2.  **綠燈 (Green)：實作最小限度功能程式碼。**
    * 只寫**剛好能讓剛才寫的 BDD 測試通過**的最基本代碼，不要過度設計或提前優化。
    * 推進測試燈號變為綠燈。

3.  **重構 (Refactor)：在測試保護下持續優化。**
    * 當測試通過（綠燈）後，著手優化功能代碼（例如提升效能、增強設計）及測試代碼（例如抽取 Test Helpers）。
    * 重構期間確保所有的測試皆維持綠燈通過狀態。

## 測試設計思考框架 (Thinking Framework)

在規劃與生成測試時，請引導自己或使用者思考以下面向，以確保產出高價值的測試代碼：

* TDD 先行視角: 我們是否已經清楚定義了輸入與預期行為，還是急著跳入實作？測試能否作為先行規格？
* 情境外展 (Coverage): 除了典型成功路徑 (`_NormalCase`)，我們是否遺漏了空值、極值 (`_EdgeCase`) 或錯誤處理 (`_ErrorCase`) 的情境？
* 可讀性與自我對話:
  * 看到 `t.Run` 的名稱，能直接說出這是一個什麼樣的業務場景嗎？ (Given-When-Then)
  * 當測試失敗時，斷言訊息 (Assertion messages) 能立刻告訴同事「發生了什麼事」嗎？
  * 變數命名 (如 `expected...` 與 `actual...`) 是否讓斷言比對一目了然？
* 獨立與純粹:
  * 各個場景 (`t.Run`) 是否完全獨立且可並行跑 (`t.Parallel()`)？
  * Mock 的狀態範圍是否足夠小 (gomock.Controller 限制在 `t.Run` 內)？
  * 我們是否為了「程式碼好看」而過度抽取了不必要的輔助函數，反而隱藏了細節？
