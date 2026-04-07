# API

## CHANGELOG

- 2025-04-07 v1.0.0 王小明 — 初始版本，建立 UserService 與 OrderService CRUD

---

## SERVICE: UserService

### DESCRIPTION
負責管理平台的使用者帳號生命週期，包含註冊、資料維護與刪除。
提供給前台 App 與後台管理系統使用。

### SERVERS
- stg: https://api.stg-user.com
- prod: https://api.prod-user.com

---

### PATH: POST /users
description: 建立使用者

#### REQUEST

##### PARAMETERS
none

##### HEADERS
| name          | required | description       |
| ------------- | -------- | ----------------- |
| Authorization | true     | Bearer token      |

##### BODY
format: application/json

| name  | type   | required | description |
| ----- | ------ | -------- | ----------- |
| name  | string | true     | 使用者名稱  |
| email | string | true     | 電子郵件    |

##### CURL
```bash
curl -X POST https://api.stg-user.com/users \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{ "name": "John Doe", "email": "john@example.com" }'
```

#### RESPONSES

##### STATUS: 201
description: 建立成功
```json
{ "id": "124", "name": "John Doe", "email": "john@example.com" }
```

##### STATUS: 400
description: 請求錯誤
```json
{
  "error": {
    "code": 4001,
    "message": "Invalid input"
  }
}
```

---

### PATH: GET /users/{id}
description: 取得使用者資料

#### REQUEST

##### PARAMETERS
| name           | in    | required | type    | description      |
| -------------- | ----- | -------- | ------- | ---------------- |
| id             | path  | true     | string  | 使用者 ID        |
| includeProfile | query | false    | boolean | 是否包含個人資料 |

##### HEADERS
| name          | required | description  |
| ------------- | -------- | ------------ |
| Authorization | true     | Bearer token |

##### BODY
none

##### CURL
```bash
curl -X GET https://api.stg-user.com/users/{id}?includeProfile=true \
  -H "Authorization: Bearer <token>"
```

#### RESPONSES

##### STATUS: 200
description: 成功取得資料
```json
{ "id": "123", "name": "John Doe", "email": "john@example.com" }
```

##### STATUS: 404
description: 找不到使用者
```json
{
  "error": {
    "code": 4002,
    "message": "User not found"
  }
}
```

---

### PATH: PUT /users/{id}
description: 更新使用者

#### REQUEST

##### PARAMETERS
| name | in   | required | type   | description |
| ---- | ---- | -------- | ------ | ----------- |
| id   | path | true     | string | 使用者 ID   |

##### HEADERS
| name          | required | description  |
| ------------- | -------- | ------------ |
| Authorization | true     | Bearer token |

##### BODY
format: application/json

| name  | type   | required | description |
| ----- | ------ | -------- | ----------- |
| name  | string | false    | 使用者名稱  |
| email | string | false    | 電子郵件    |

##### CURL
```bash
curl -X PUT https://api.stg-user.com/users/{id} \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Jane Doe", "email": "jane@example.com" }'
```

#### RESPONSES

##### STATUS: 200
description: 更新成功
```json
{ "id": "123", "name": "John Doe", "email": "john@example.com" }
```

##### STATUS: 404
description: 找不到使用者
```json
{
  "error": {
    "code": 4002,
    "message": "User not found"
  }
}
```

---

### PATH: DELETE /users/{id}
description: 刪除使用者

#### REQUEST

##### PARAMETERS
| name | in   | required | type   | description |
| ---- | ---- | -------- | ------ | ----------- |
| id   | path | true     | string | 使用者 ID   |

##### HEADERS
| name          | required | description  |
| ------------- | -------- | ------------ |
| Authorization | true     | Bearer token |

##### BODY
none

##### CURL
```bash
curl -X DELETE https://api.stg-user.com/users/{id} \
  -H "Authorization: Bearer <token>"
```

#### RESPONSES

##### STATUS: 204
description: 刪除成功
```json
{}
```

##### STATUS: 404
description: 找不到使用者
```json
{
  "error": {
    "code": 4002,
    "message": "User not found"
  }
}
```

---

## SERVICE: OrderService

### DESCRIPTION
處理訂單的建立、狀態追蹤與取消流程。
由 UserService 驗證使用者身份後呼叫。

### SERVERS
- stg: https://api.stg-order.com
- prod: https://api.prod-order.com

---

### PATH: POST /orders
description: 建立訂單

#### REQUEST

##### PARAMETERS
none

##### HEADERS
| name          | required | description       |
| ------------- | -------- | ----------------- |
| Authorization | true     | Bearer token      |
| X-Request-Id  | false    | 追蹤用 request ID |

##### BODY
format: application/json

| name      | type   | required | description |
| --------- | ------ | -------- | ----------- |
| user_id   | string | true     | 使用者 ID   |
| item_id   | string | true     | 商品 ID     |
| quantity  | number | true     | 數量        |

##### CURL
```bash
curl -X POST https://api.stg-order.com/orders \
  -H "Authorization: Bearer <token>" \
  -H "X-Request-Id: req-abc123" \
  -H "Content-Type: application/json" \
  -d '{ "user_id": "124", "item_id": "item456", "quantity": 2 }'
```

#### RESPONSES

##### STATUS: 201
description: 建立成功
```json
{ "order_id": "abc123", "status": "pending" }
```

##### STATUS: 400
description: 請求錯誤
```json
{
  "error": {
    "code": 4001,
    "message": "Invalid input detail"
  }
}
```

##### STATUS: 404
description: 找不到使用者或商品
```json
{
  "error": {
    "code": 4002,
    "message": "User or item not found"
  }
}
```

---

### PATH: GET /orders/{order_id}
description: 取得訂單資料

#### REQUEST

##### PARAMETERS
| name      | in   | required | type   | description |
| --------- | ---- | -------- | ------ | ----------- |
| order_id  | path | true     | string | 訂單 ID     |

##### HEADERS
| name          | required | description  |
| ------------- | -------- | ------------ |
| Authorization | true     | Bearer token |

##### BODY
none

##### CURL
```bash
curl -X GET https://api.stg-order.com/orders/{order_id} \
  -H "Authorization: Bearer <token>"
```

#### RESPONSES

##### STATUS: 200
description: 成功取得訂單
```json
{ "order_id": "abc123", "user_id": "124", "item_id": "item456", "quantity": 2, "status": "pending" }
```

##### STATUS: 404
description: 找不到訂單
```json
{
  "error": {
    "code": 4002,
    "message": "Order not found"
  }
}
```

---

### PATH: PUT /orders/{order_id}
description: 更新訂單狀態

#### REQUEST

##### PARAMETERS
| name      | in   | required | type   | description |
| --------- | ---- | -------- | ------ | ----------- |
| order_id  | path | true     | string | 訂單 ID     |

##### HEADERS
| name          | required | description  |
| ------------- | -------- | ------------ |
| Authorization | true     | Bearer token |

##### BODY
format: application/json

| name    | type   | required | description                          |
| ------- | ------ | -------- | ------------------------------------ |
| status  | string | true     | 訂單狀態（pending / shipped / done） |

##### CURL
```bash
curl -X PUT https://api.stg-order.com/orders/{order_id} \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{ "status": "shipped" }'
```

#### RESPONSES

##### STATUS: 200
description: 更新成功
```json
{ "order_id": "abc123", "status": "shipped" }
```

##### STATUS: 404
description: 找不到訂單
```json
{
  "error": {
    "code": 4002,
    "message": "Order not found"
  }
}
```

---

### PATH: DELETE /orders/{order_id}
description: 取消訂單

#### REQUEST

##### PARAMETERS
| name      | in   | required | type   | description |
| --------- | ---- | -------- | ------ | ----------- |
| order_id  | path | true     | string | 訂單 ID     |

##### HEADERS
| name          | required | description  |
| ------------- | -------- | ------------ |
| Authorization | true     | Bearer token |

##### BODY
none

##### CURL
```bash
curl -X DELETE https://api.stg-order.com/orders/{order_id} \
  -H "Authorization: Bearer <token>"
```

#### RESPONSES

##### STATUS: 204
description: 取消成功
```json
{}
```

##### STATUS: 404
description: 找不到訂單
```json
{
  "error": {
    "code": 4002,
    "message": "Order not found"
  }
}
```
