# 前端 / UI issue

## Environment

- 作業系統與版本
- 瀏覽器與完整版本號（`Chrome 131.0.6778.86`，不是「最新版」）
- 裝置類型與解析度（RWD 問題必填）
- 應用版本或 build number
- 登入狀態與帳號角色——權限不同常導致行為不同
- 特殊條件：無痕模式、擴充套件、網路狀況、語系

跨瀏覽器問題要註明**測過但不會發生的組合**：「Chrome 有、Safari 沒有」的資訊量遠大於「Chrome 有」。

## Steps to Reproduce

編號、每步一個動作，前置條件寫在第一步之前。寫完自己走一次：沒看過這系統的人照做，會不會卡在某個沒寫出來的前提（要先有資料？要特定權限？要清 cache？）。

超過 10 步通常代表中間有無關步驟可刪，或前置狀態可以用「帳號 A 已有 3 筆未結訂單」一次交代掉。

最後註明重現機率：每次都會 / 約一半 / 只遇過一次。

## Evidence

- 截圖標出問題位置，不要只丟整頁截圖
- 互動或動畫問題用螢幕錄影
- 附 console error 與 network tab 的失敗請求（status code、response body）
- 樣式問題附 computed style 或 DOM 片段

## 範例

~~~markdown
# Submit button 在 checkout page 無回應（購物車超過 50 項時）

## Summary
購物車項目數超過 50 時，checkout page 的 submit button 點擊後無任何反應，
也無錯誤提示。使用者無法完成結帳，且不知道發生了什麼事。

## Environment
- macOS 15.2 / Chrome 131.0.6778.86
- App version 4.12.3（build 2891）
- 一般會員帳號，已登入
- Safari 18.2 與 Firefox 133 同樣可重現，非瀏覽器限定

## Steps to Reproduce
前置條件：測試帳號 `qa-user-07`，購物車已加入 51 項商品。
1. 進入 `/checkout`
2. 填妥收件資訊與付款方式
3. 點擊「送出訂單」
4. 觀察：按鈕無 loading 狀態，頁面無變化

重現機率：100%（試 5 次皆同）。項目數降至 50 以下即恢復正常。

## Expected vs Actual
- **Expected**：送出訂單並導向訂單完成頁
- **Actual**：無任何回應，頁面停留原地，未顯示錯誤訊息

## Impact
影響所有購物車超過 50 項的使用者（約佔下單流量 2%，多為企業採購帳號）。
現有 workaround 是分批下單，但使用者無從得知。

## Evidence
```
POST /api/v1/orders → 413 Payload Too Large
console: Uncaught (in promise) TypeError: Cannot read properties of undefined (reading 'orderId')
```

## Severity / Priority
- **Severity**：Major — 核心流程阻斷，且無錯誤提示
- **Priority**：High — 直接影響營收，受影響的是高客單價帳號
~~~
