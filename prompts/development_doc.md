# Development Requirements Document

標準化撰寫一份技術開發需求文件

主要分為 4 個部分
- Glossary
- PRD
- SRS
- TSD

PRD(why,who) + SRS(what) + TSD(how) 文件涵蓋了從「為什麼做」、「做什麼」到「怎麼做」的完整流程

PRD Scope 設定了大方向和邊界

SRS 填充細節，讓開發和測試團隊知道具體要實現哪些功能行為

SRS 是面向需求的，定義「需要建造一個什麼樣的系統」，是 TSD 的輸入。  
TSD 是面向技術實現的，定義「要如何建造這個系統」，是 SRS 的輸出/實現方案。  

開發者看著 SRS 知道目標是什麼，然後設計並撰寫 TSD 來規劃如何達成這個目標，最後依據 TSD 來進行編碼實作。  

## Prompt Reference

[Kafka Improvement Proposals](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals)

---

## Glossary

描述產品的各個元素，不是讓讀者猜測或誤解技術規格，以表格的方式呈現 `Term`, `Meaning`

## PRD（Product Requirements Document）

1. 背景與痛點（Problem）  
   - 使用者遇到什麼問題？  
   - 為什麼這個功能現在需要做？

2. 解決目標（Objectives）  
   - 我們期望透過這個功能達成什麼結果？（商業 / 使用者體驗）
   - 目標使用者是誰、需要具備哪些功能來滿足市場或使用者需求

3. 功能範圍（Scope）  
   - 定義功能、產品或特定版本的邊界
   - 高層次的交付物、主要功能模組或特性（用簡單語言條列）
   - 回應 PRD 前面定義的「解決目標（Objectives）」，目標是「要去哪裡」，範圍就是「要走哪些路、建哪些東西才能到」
   - 「這次要做哪些主要的部分？」以及「不包含哪些部分？」，例如：「本次重構不包含資料庫 Schema 的變更。」

## SRS（Software Requirements Specification）

1. Functional Requirements  
   - 各個功能點的細節與邏輯  
   - 對外提供的 API 定義（方法、參數、回傳格式）  
   - 更貼近「系統必須做什麼」的描述，使其更具體且可測試。
       - FR-01: CLI 工具必須能夠接收並解析 -p (partitions), --pWorker, --tWorker, --datetime, --conf, -d 等參數。
        - FR-02: CLI 工具必須能根據 --conf 參數或預設路徑/環境變數載入設定檔（例如 velo.yml）。

2. Non-Functional Requirements  
   - 效能：QPS、延遲上限  
   - 安全性：認證、權限檢查  
   - 可用性 / 可維護性  
   - 資料一致性需求（例如 eventual / strong consistency）

3. Force 設計限制 (Design Constraints)  
   - 任何限制開發選擇的因素，例如：必須使用 Golang 開發。必須能在 Linux 環境執行

4. 驗收條件（Acceptance Criteria）  
   - 功能如何算是「完成」？有沒有可量化或可驗證的條件？
   - 基於規則的清單格式（Rule-oriented / Checklist format）
       - 格式：`確認 [某個條件] 。` / `驗證 [某個行為發生] 。` / `檢查 [某個結果正確] 。`
   - 基於場景的格式（Scenario-oriented format / Given/When/Then）
        * Given：描述一個初始的上下文或前提條件。
        * When：描述觸發事件或使用者執行了某個動作。
        * Then：描述預期的結果或系統應有的反應。（可以有多個 `And` 或 `But` 來補充結果）

## TSD（Technical Specifications Document）

TSD 主要描述「如何」實現 SRS 中定義的需求。

1. 架構設計（System Architecture）  
   - 有沒有新的 component/service 要加？  
   - 跟哪些既有系統整合？

2. 技術選型與理由（Tech Stack Decisions）  
   - 使用哪個資料庫？選用哪個第三方套件？為什麼？

3. 資料流程與時序圖（Data Flow / Sequence Diagram / State Diagram）  
   - 使用者操作 → 系統內部處理流程  
   - 內部 service 間資料流、MQ、DB 的存取順序

4. 潛在風險與對策（Risks and Mitigations）  
   - 有什麼難點或不確定性？怎麼先處理？
