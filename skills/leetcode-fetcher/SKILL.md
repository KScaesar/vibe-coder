---
name: leetcode-fetcher
description: 從 LeetCode 題目 URL 或 title slug 自動抓取並解析題目內容，包含題目描述、難度、Tags、提示（Hints）與相關題目列表。當使用者提供 LeetCode 題目連結（例如 https://leetcode.com/problems/two-sum/）或 slug（例如 two-sum）時使用此技能，以避免使用者手動複製貼上題目內容。本技能會呼叫 LeetCode 公開的 GraphQL API（不需登入），取得格式化後的 Markdown 題目資訊，供後續演算法分析、面試準備使用（可搭配 algo-interview-prep 技能）。
---

# LeetCode 題目抓取器 (LeetCode Problem Fetcher)

## 工作流程

當使用者提供 LeetCode URL 或 slug 時：

### 1. 執行抓取腳本

使用隨附的 `scripts/fetch_problem.py` 腳本抓取題目資訊：

```bash
uv run <absolute-path-to-skill>/scripts/fetch_problem.py <url-or-slug>
```

**支援格式：**

- 完整 URL：`https://leetcode.com/problems/number-of-islands/`
- 題目 slug：`number-of-islands`

腳本會透過 LeetCode 公開 GraphQL API (`https://leetcode.com/graphql`) 取得資料，**無需登入或 Cookie**。

### 2. 輸出內容

腳本輸出以下欄位（Markdown 格式）：

- 題目編號、標題、難度（🟢🟡🔴）
- Topic Tags
- 完整題目描述（HTML → 純文字）
- 提示 (Hints)
- 相關題目 (Similar Questions)

### 3. 後續整合

抓取完成後，可直接將輸出餵給 `algo-interview-prep` 技能進行分析與解題引導。

## 注意事項

- LeetCode Premium 題目可能因未登入而回傳 `null` 內容，此時會顯示「找不到題目」。
- 速率限制：避免短時間內大量請求。
