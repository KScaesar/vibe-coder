---
name: leetcode-fetcher
description: 當使用者提供題目連結、題目識別名稱，或直接以純文字描述題目時，必須自行取得並解析題目內容，減少使用者手動複製貼上題目敘述；若可自動解析則以解析結果為準，否則直接以使用者提供的文字描述作為題目來源，再進行後續分析與分類。可搭配 algo-interview-prep 技能進行解題引導。本技能的核心任務是「自動化環境建立與測試案例準備」，Agent 應僅限於建立正確的檔案目錄與測試代碼，**嚴禁在此階段自動撰寫解題逻辑**。
---

# LeetCode 題目抓取器

## Step 1：抓取題目

依 URL 來源選擇對應腳本（將 `<skill-path>` 替換為本技能的絕對路徑）：

| 來源           | 指令                                                          |
| -------------- | ------------------------------------------------------------- |
| `leetcode.com` | `uv run <skill-path>/scripts/fetch_leetcode.py <url-or-slug>` |
| `neetcode.io`  | `uv run <skill-path>/scripts/fetch_neetcode.py <url>`         |
| 其他 / 未知    | `uv run <skill-path>/scripts/fetch_generic.py <url>`          |

- **LeetCode / NeetCode**：腳本輸出 `=== LEETCODE_FILE_CONTENT_START/END ===` 之間的完整 Python 基礎結構，直接作為檔案基底。
- **其他來源 / 純文字描述**：若使用者直接提供題目文字而無 URL，Agent 應略過執行腳本，改由 AI 自行組裝完整 Python 檔案內容（包含 Docstring 描述與解決方案類別）。
- 若動態頁面抓取失敗，改用內建 `web_fetch` 或 `playwright` 技能。
- **重要原則**：Agent 在此階段應保持 `Solution` 類別內的方法為 `pass` 或維持腳本輸出的原始狀態。**絕對不要擅自寫入有效解法**。

---

## Step 2：分類題目

閱讀題目描述，依**核心解題邏輯**（非 Tags 關鍵字）歸類至以下其中一類：

- Arrays & Hashing
- Two Pointers
- Sliding Window
- Stack: 解法依賴 LIFO 處理配對、近期狀態或巢狀結構時才歸此類
- Binary Search
- Linked List
- Trees
- Heap / Priority Queue
- Backtracking
- Tries
- Graphs
- Advanced Graphs
- 1-D Dynamic Programming
- 2-D Dynamic Programming
- Greedy
- Intervals: 核心在於處理區間關係（合併、重疊、掃描）才歸此類
- Math & Geometry
- Bit Manipulation

---

## Step 3：建立檔案

**檔名規則：**

| 情境           | 格式                                     | 範例                               |
| -------------- | ---------------------------------------- | ---------------------------------- |
| LeetCode       | `{五碼ID}._{Title_Case}.py`              | `00001._Two_Sum.py`                |
| Weekly Contest | `Contest{期數}_Q{第N題}_{Title_Case}.py` | `Contest491_Q1_Count_Subarrays.py` |
| 其他           | `00000._{Title_Case}.py`                 | `00000._Target_Sum.py`             |

特殊符號以底線替換，並清除多餘底線。

**檔案結構：** 腳本輸出的基礎結構（Docstring + Solution class）＋ 手動補充的測試區塊：

```python
def main():
    solution = Solution()

    # Case 1
    # assert solution.searchRange([5,7,7,8,8,10], 8) == [3,4]

    # Case 2
    # assert solution.searchRange([5,7,7,8,8,10], 6) == [-1,-1]

    print("All tests passed!")

if __name__ == "__main__":
    main()
```

> ⚠️ 測試值必須填入範例的**實際數值**，禁止使用 `EXPECTED_RESULT` 佔位符。

**寫入路徑：** `<cwd>/<Category_Name>/<檔名>`

---

## Step 4：後續整合（選用）

完成後可將檔案內容交給 `algo-interview-prep` 技能進行解題引導。
