---
name: layer-review
description: 以 DDD 與 Hexagonal Architecture（Ports and Adapters）的分層視角審查一段程式碼變更，依 Domain／Application／Infrastructure／User Interface 分組，指出安全、效能、可維護性風險並提出具體改善，產出 zh-TW Markdown 審查報告。使用者提到 code review、review 這個 commit／PR／branch、比較兩個 commit、「幫我看這次改了什麼、有沒有問題」、分層審查、架構審查、新人要看懂這次變更時使用——即使原始碼本身沒有照 DDD 分層也適用。不適用於：只想除錯或找單一 bug 的 root cause、部署並行風險（用 rolling-deploy-review）、撰寫 commit message 或 PR 說明。
---

# 分層架構 Code Review

## 為什麼要分層看

逐檔 review 容易陷在細節裡，看不出「這次變更讓業務規則滲進了 adapter」或「domain 開始依賴某個 framework」。先把每一處變更歸到它**實際扮演的角色**，再逐層評估，架構腐化與責任錯置才會浮現。原始碼的目錄結構不代表它的角色——`service/` 底下可能同時有 use case 與 SQL，照行為分，不照資料夾分。

假設自己第一次接觸這個 codebase，讀者則是剛加入的新成員。

## 輸入

- **範圍**：使用者可能給兩個 commit、一個 branch、PR 編號、或只說「目前的改動」。自行決定如何取得 diff 與周邊脈絡；範圍模糊時用最合理的解讀並在報告 metadata 寫明，真的無法判斷才詢問。
- **`detail`**：`true` 時附上逐檔摘要；未指定視為 `false`。

理解變更時，遵循專案 AGENTS.md 的 code intelligence 原則：優先用結構化工具（LSP、go-to-definition、find-references）確認 symbol 的定義與呼叫端，只拉需要的上下文。一段改動的風險常在呼叫端，而不在 diff 本身。

## 分層歸類

| Layer | 角色 |
|---|---|
| Domain | 業務規則：entity、value object、aggregate、domain service、invariant |
| Application | Use case 編排、transaction 邊界、呼叫 port |
| Infrastructure | DB、外部 API、messaging、framework 設定、persistence、logging |
| User Interface | HTTP handler、CLI、UI、message consumer／producer 的進出口 |

同一個檔案可能橫跨多層，拆開歸類並指出這本身是否是問題。

## 每層要評估什麼

以下是每個 layer 都要逐一檢查的角度。每個角度都要看過；有發現就寫，沒發現的角度不必為了填滿而寫「無」：

- **變更性質**：新功能、bug fix、refactor、optimization
- **風險**：安全漏洞、正確性、邊界條件、錯誤處理——附改善建議
- **依賴方向**：是否違反「外層依賴內層」；domain 是否引入 framework 或 I/O
- **邊界洩漏**：adapter 是否直接暴露 domain 結構——例如把 entity 直接序列化成 API 回應、訊息 payload 或 DB schema，讓內部模型變成對外契約；應以 DTO／mapper 隔開
- **SOLID 與 pure function**：副作用是否被推到邊界
- **過度設計**：不必要的抽象、premature optimization、可以更簡單的寫法

### 效能

依系統的工作負載評估，不確定是哪一種時說明判斷依據：

- **OLTP**：concurrency、lock、index、query latency、CPU／IO
- **OLAP**：partition、大量資料的 query 最佳化、memory、parallelism

建議要務實——維護成本與效能收益一起權衡，不要為了假想的規模過度工程化。

## 證據原則

每個指出的問題都要能回指到具體檔案與程式碼。看不出意圖或缺少脈絡時，寫明「需要確認什麼、為什麼」，不要用猜測補空白；把推測寫成結論會讓整份報告失去可信度。

## 輸出

篇幅以中等為宜、語氣正式。儘可能列出所有找到的問題——低嚴重度的也要列，一行帶過即可；漏掉一個問題的代價，遠高於讀者多看一行。篇幅靠每一項寫得精簡來控制，而不是刪減項目：講清楚「哪裡、為什麼有風險、怎麼改」即可；程式碼範例只在文字說不清楚時才附，並保持最短。

### 範圍內與範圍外

- **範圍內**：本次變更本身，以及它造成的影響——即使缺陷出現在沒被修改的檔案（例如改了 handler，導致既有 use case 存錯資料），也歸在缺陷所在的 layer 段落。
- **範圍外**：與本次變更無關、原本就存在的問題。只列審查過程中看到的，不必另外全面掃描 codebase；統一放在報告最後的 `## 範圍外的既有問題`，不要混進 layer 段落，也不要為它另開 layer 標題。同樣遵守證據原則。

### 格式

以 zh-TW 撰寫，存成工作目錄下的 `review_<new commit 前 8 碼>.md`（沒有 commit 可用時，例如未提交的改動或無法解析的 commit，改用 `review_<YYYYMMDD-HHMM>.md`）。檔案路徑一律以 `./path/to/file` 呈現。

```markdown
datetime: <執行當下時間，含時區，例如 2026-09-23 14:05 +0800>
scope: <比較範圍，commit 取前 8 碼，例如 old=12ab34cd vs new=56ef78gh；未提交改動寫 old=12ab34cd vs new=working tree>

## Domain Layer
- <變更與問題條列，附 ./path/to/file>

### Analysis
<分析與建議>

## Application Layer
...

## Infrastructure Layer
...

## User Interface Layer
...

## File Change Summaries
- ./path/to/file: <兩句話說明改了什麼、為什麼>

## 範圍外的既有問題
- <問題條列，附 ./path/to/file>
```

- 只列出有變更或受本次變更影響的 layer。
- `## File Change Summaries` 只在 `detail=true` 時出現。
- `## 範圍外的既有問題` 沒有內容時省略；有的話永遠是最後一段。
- 無法取得 diff 或內容時，不要產出空殼報告：在 metadata 後只放 `## Error`，說明失敗的原因與需要使用者提供什麼。
