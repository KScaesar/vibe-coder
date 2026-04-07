---
name: api-markdown
description: >
  撰寫可供 Google Apps Script（GAS）穩定解析的 API 文件，格式為結構化 Markdown。
  當使用者要寫 API 文件、設計 REST API spec、記錄多個服務的 CRUD 端點、
  或需要讓程式自動讀取 API 文件時，請使用此 skill。
  也適用於使用者說「幫我寫 API 文件」、「定義 endpoint」、「記錄這個服務的 API」的情境。
---

# API Markdown Skill

結構化 Markdown 格式，設計給人類速讀、GAS 穩定解析兩者兼顧。

**完整範例請見** `references/example.md`（多服務 CRUD 完整示範）

---

## 設計原則

1. **Header 層級固定** — 每一層只有固定幾個關鍵字，不自由命名
2. **關鍵字全大寫** — 與自然語言文字明確區分
3. **`none` 統一代表「無」** — 不用中文、不留空白區塊
4. **key-value 格式** — `key: value`，一行一條，不用自由文字段落
5. **`####` 只有兩個值** — `REQUEST` 和 `RESPONSES`，不混用

---

## Header 層級樹

```
# API
├── ## CHANGELOG
└── ## SERVICE: <ServiceName>
    ├── ### DESCRIPTION
    ├── ### SERVERS
    └── ### PATH: <METHOD> <path>   ← 一個 PATH 只有一個 METHOD
        │   description: <說明>
        ├── #### REQUEST
        │   ├── ##### PARAMETERS
        │   ├── ##### HEADERS
        │   ├── ##### BODY
        │   └── ##### CURL
        └── #### RESPONSES
            └── ##### STATUS: <code>
                    description: <說明>
                    ```json
                    { ... }
                    ```
```

---

## 各層寫法

### `## CHANGELOG`

放在所有 SERVICE 之前。純人類可讀，每行一筆，bullet list 格式。
格式為 `- <日期> <版本> <作者> — <說明>`。

```markdown
## CHANGELOG

- 2025-04-07 v1.2.0 王小明 — 新增 GET /orders/{order_id}
- 2025-03-01 v1.1.0 陳大華 — 修改 POST /users 新增 email 欄位
```

---

### `## SERVICE: <ServiceName>`

服務名稱接在關鍵字後，同一行。用來識別服務邊界。

```markdown
## SERVICE: UserService
```

---

### `### DESCRIPTION`

說明這個服務存在的目的、背景、或使用情境。幫助讀者理解 API 的來龍去脈。
不需要說明時寫 `none`。

```markdown
### DESCRIPTION
負責管理平台的使用者帳號生命週期，包含註冊、資料維護與刪除。
提供給前台 App 與後台管理系統使用。
```

---

### `### SERVERS`

每個環境一行，bullet list 格式，`env: url`。

```markdown
### SERVERS
- stg: https://api.stg-example.com
- prod: https://api.prod-example.com
```

---

### `### PATH: <METHOD> <path>`

METHOD 全大寫。`description` 接在 header 下一行，說明這支 API 做什麼事。

> ⚠️ **一個 `### PATH` 只能有一個 METHOD。**
> 絕對不可寫成 `### PATH: PATCH GET /users/{id}` 或 `### PATH: POST PATCH /orders`。
> 不同的 method 必須各自獨立成一個 `### PATH` 區塊。

```markdown
### PATH: POST /users
description: 建立使用者
```

❌ 錯誤範例（絕對不可這樣寫）：
```markdown
### PATH: PATCH GET /users/{id}
### PATH: POST PATCH /orders
```

✅ 正確做法（每個 method 獨立一個 PATH 區塊）：
```markdown
### PATH: GET /users/{id}
description: 取得使用者資料

### PATH: PATCH /users/{id}
description: 部分更新使用者資料
```

---

### `#### REQUEST`

固定關鍵字，底下固定四個子區塊：`PARAMETERS`、`HEADERS`、`BODY`、`CURL`。

---

### `##### PARAMETERS`

query / path 參數。無時寫 `none`。
`in` 欄位值只有兩種：`path` / `query`。

```markdown
##### PARAMETERS
none
```

```markdown
##### PARAMETERS
| name | in    | required | type    | description |
| ---- | ----- | -------- | ------- | ----------- |
| id   | path  | true     | string  | 使用者 ID   |
| q    | query | false    | string  | 搜尋關鍵字  |
```

---

### `##### HEADERS`

Request header。無時寫 `none`。

```markdown
##### HEADERS
| name          | required | description       |
| ------------- | -------- | ----------------- |
| Authorization | true     | Bearer token      |
| X-Request-Id  | false    | 追蹤用 request ID |
```

---

### `##### BODY`

Request body schema。無時寫 `none`。
`format:` 宣告 content-type，下接欄位 table。

```markdown
##### BODY
format: application/json

| name  | type   | required | description |
| ----- | ------ | -------- | ----------- |
| name  | string | true     | 使用者名稱  |
| email | string | true     | 電子郵件    |
```

---

### `##### CURL`

可直接執行的 curl 範例，使用 stg 環境 URL。
從 SERVERS、HEADERS、BODY 的資訊組出來，方便快速測試。

```markdown
##### CURL
```bash
curl -X POST https://api.stg-example.com/users \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{ "name": "John Doe", "email": "john@example.com" }'
```
```

---

### `#### RESPONSES`

固定關鍵字，底下接一或多個 `##### STATUS`。

---

### `##### STATUS: <code>`

Status code 接在關鍵字後，同一行。
`description` 在下一行說明此狀態的意義。
JSON response 接在 description 後的 code block。
無 response body 時，code block 寫 `{}`。

```markdown
##### STATUS: 201
description: 建立成功
```json
{ "id": "124", "name": "John Doe" }
```

##### STATUS: 400
description: 請求錯誤
```json
{ "error": "Invalid input" }
```
```

---

## 視覺分隔

`---` 水平線用來在 SERVICE 之間、PATH 之間增加視覺間距，方便人類閱讀，不影響解析。
建議在每個 `## SERVICE` 和每個 `### PATH` 結束後加上 `---`。
