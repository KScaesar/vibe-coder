---
name: doc-validator
description: 驗證與審核技術文件的結構、內容歸屬、粒度與可用性，並給出信心指數（預設 >= 90% 合格）。只要使用者要審查、review、audit、lint 或重構 / 遷移文件（例如把單一大檔拆成多份文件），檢查 README / 文件首頁是否過於肥大或缺少導航，判斷某份文件該放在哪個目錄、是否內容混雜或過度碎片化需要合併 / 拆分，規劃 docs/ 目錄結構，或審查 ADR 與測試驗收規格的歸屬時，就使用本技能，即使使用者沒有明確說「validator」。
---

# doc-validator

驗證文件是否把「對的內容放在對的地方，並保持適度粒度」，且讀者實際用得起來。核心做法：每份文件先歸類並評估粒度，再做機械檢查與讀者情境走查，最後輸出違規清單與搬移 / 拆分 / 合併建議。

只看「歸類是否正確」不夠：歸類對、內容卻在搬移中遺失，或讀者仍找不到東西，都是不合格。所以本技能同時檢查內容歸屬、來源保真、讀者可用性三件事。

**判定標準分兩級**（全文統一用這個說法）：
- **硬規則**：只有 Migration 的兩條 ——「省略清單出現『其他』」與「有未解決的『更差』區塊」，出現即不合格。
- **裁量**：其餘一切（歸類、粒度、Checklist、數字訊號）依商業邏輯與讀者情境判斷，看是否影響讀者找到、讀懂、做完；數字只是提示。

每條規則只在一處定義，其他章節與 references 僅引用。

## Core Principles

- **單一職責**：一份文件只服務一種讀者需求。混雜會讓讀者在需要時找不到、在不需要時被干擾。
- **單一事實來源（Single Source of Truth，SSOT）**：每個事實只在一份文件中完整定義，該文件即為它的權威來源；其他文件需要時只引用並連結回來源，不另存副本。副本一旦與來源各自演進，就會產生互相矛盾的說法，讀者無從判斷哪個才對。允許少量連結式交叉說明（一兩句點出關聯並連回來源），不算違反 SSOT。
- **粒度雙向裁量**：拆分混雜內容的同時，也要避免兩個極端，以閱讀順暢、心智負擔最低為準。
  - 過度碎片化：同類型且緊密關聯的小主題應優先合併。訊號：同一概念散在 ≥3 檔、完成一個任務需開 ≥4 個必要檔、單檔 <20 行且只有指標。「必要檔」計法：首頁計 1，其餘導覽頁、索引頁不計（否則導覽越完善反而越被扣分），細則見 [references/reader-walkthrough.md](references/reader-walkthrough.md)。
  - 過度合併：合併後單檔過長且多主題（約 >200 行）、或合併造成自我連結，同樣要拆。
  - 最終以「依序讀完一個主題要開幾個必要檔、來回跳轉幾次」判斷。
- **導航不承載內容**：intent-doc 只做分流與跳轉。橫切索引只列項目與一句話並連到來源；索引中若整理出新的規則表，就算整合型文章，需有授權或逐句可溯源。
- **命名一致**：目錄與檔名風格統一，預設全小寫；`README.md`、ADR 編號檔等通行慣例不算違規。四象限目錄名以 tutorials、guides、reference、explanation 為準，`how-to` 等官方同義命名只要全專案一致，不判違規。其餘目錄為 decisions、testcases。

## Document Types

### Part 1: Intent-doc

來源：自訂設計，不屬於 Diataxis，Diataxis 本身沒有規定讀者動線。

intent-doc 是中央路由器，載體為文件首頁 `index.md` 或倉庫根目錄 `README.md`。目標：讀者 10 秒內完成意圖分流。

**必備**（審查只檢查這兩項）：
1. **一句話定位**：這是什麼、給誰用、解決什麼問題。第一次接觸的讀者沒有這句就無從判斷要不要往下讀。小型專案（單一工具或文件少於 5 份）也不可省略。
2. **三條路徑的入口找得到**：explanation（Top-down）、tutorials（Bottom-up）、guides（Task-driven）能從首頁或 README 找到，且入口文件有連結通往圖中的跳轉目標。小型專案可省略部分入口，不應僅因路徑不全就扣分。

**建議**（不要求照抄）：Hero 雙軌入口（tutorials 與 explanation 並列）、任務路由表（常見任務對應 guides）、四象限全域目錄、通往 decisions/ 與 testcases/ 的治理入口。

**倉庫根目錄 `README.md`** 是精簡版：一句話定位、極簡 quickstart、架構摘要與各目錄跳轉連結，不貼全量 API 字典或完整安裝手冊。審查 README 只看：是否肥大、有無一句話定位、能否連到三類入口。

**三條閱讀路徑**：`entry` 是入口，`flow` 是建議順序（非強制）。箭頭編號是離開當前文件的原因：(1) 想確認是否適用，(2) 已有手感要處理真實情境，(3) 需確認精確規格，(4) 想知道為何這樣運作，(5) 遇到例外或極端情境。

```text
[Top-down]    先全貌、後細節（評估工具、接手新領域）；Top-down 讀者不應被迫先動手練習
  entry : explanation
  flow  : explanation --(1)--> guides --(3)--> reference --(5)--> explanation

[Bottom-up]   先體感、後原理（照範例跑出第一個成功）
  entry : tutorials
  flow  : tutorials --(2)--> guides --(3)--> reference
                                 +--(4)--> explanation

[Task-driven] 先任務、後必要資訊（異常排查）
  entry : guides
  flow  : guides --(3)--> reference
             +--(4)--> explanation
```

另一個可用性檢查：第一次接觸者能否在必要檔數 ≤3（首頁計入）內，只靠首頁及其連結回答「這是什麼、給誰用」並找到第一個動作（計法見 [references/reader-walkthrough.md](references/reader-walkthrough.md)）。

### Part 2: Diataxis 框架

來源：
- Diataxis 官方 https://diataxis.fr/ （tutorials-how-to、reference-explanation 兩篇差異專題特別有助於判斷模糊案例）。
- Divio Documentation System https://docs.divio.com/documentation-system/introduction/ （四象限的原始介紹，提供「各類型只有一個任務」的原則與烹飪類比）。

僅包含 tutorials、guides、reference、explanation 四個象限。

核心原則：每一類文件只有一個任務，各自需要不同的寫法，必須明確分開、互不混雜。讀者在使用過程的不同階段需要不同類型的文件，混雜會讓文件被同時往多個方向拉扯。

分類原則：依「學習 vs 工作」與「行動 vs 認知」分類，而非按難度。tutorials 與 guides 的分界是「學習體驗 vs 生產任務」，不是入門 vs 進階。

下列 Must Not 皆指「內嵌大段內容」；一兩句連結式交叉說明可接受。各類型的「關鍵要素」是檢查內容有沒有涵蓋的參考，不是必須照抄的章節模板；只要大方向歸類正確、要素有被涵蓋，寫法不受限。

#### tutorials
- **Purpose**：帶新手取得第一次成功（學習 + 行動）。
- **Reader**：零心智模型，不預設工具背景與排錯能力。
- **Environment**：完全受控，固定版本與素材，無外部變數。
- **Must**：單一線性路徑；每步有預期輸出；承諾必定成功；卡住即視為文件缺陷（責任在作者）；結尾導向 guides 與 explanation；語氣溫和、陪伴式。
- **Must Not**：解釋架構原理、提供分支或替代方案、省略基礎指令、依賴未固定版本的外部資源。
- **關鍵要素**：前置準備、最小可用步驟、預期輸出驗證、下一步導流。
- **類比**：教小孩學做菜的一堂課。

#### guides
- **Purpose**：完成特定生產任務（工作 + 行動）。
- **Reader**：有基礎能力，已知目標。
- **Environment**：真實世界，含依賴衝突與不可控變數。
- **Must**：包含真實條件分支（如 Docker vs 裸機）；假設讀者有能力，不重複解釋基本指令；參數連結至 reference；需要原理說明處連結至 explanation（僅連結，不內嵌論述）；語氣專業、俐落。
- **Must Not**：列全量參數字典、論述架構演進。
- **關鍵要素**：前置條件、操作步驟（含分支）、成果驗證、疑難排解。
- **類比**：食譜書裡的一道食譜。

#### reference
- **Purpose**：提供權威、客觀的事實規格（工作 + 認知）。
- **Reader**：知道自己在查什麼。
- **Environment**：無環境依賴，結構鏡像程式碼。
- **Must**：精確、即時更新；以清單、簽名、結構化欄位呈現；條目附相關 guides 與 explanation 連結（僅連結，不內嵌論述）。
- **Must Not**：操作教學、主觀評價或建議、架構哲學。
- **注意別過度執行 Must Not**：「行為前提」是事實，應留在 reference，例如「某操作不會等待進行中的另一操作完成，呼叫端必須自行處理競態」。要移走的是「為何這樣設計」的理由與取捨，不是使用者正確使用所必須知道的行為約束。判斷方式：拿掉這句，讀者是否可能誤用？會，就留。審查者若要以「reference 含理由」判違規，必須在報告寫出這個判斷；判斷不出來就歸 C 類保留，不判違規。
- **關鍵要素**：簽名宣告、參數規格（型別 / 預設值 / 約束）、回傳結構、錯誤碼、最小調用範例。
- **類比**：百科全書中的一個條目。

#### explanation
- **Purpose**：說明系統為何如此設計與取捨（學習 + 認知）。
- **Reader**：有實作經驗，想理解全局。
- **Environment**：抽象的思考空間。
- **Must**：主題式論述；多角度與替代方案權衡；提及具體實踐或操作場景時連結至 guides；提到模組時連結其 reference；提到歷史選型時單向連結 decisions 對應的 ADR。
- **Must Not**：逐步操作指令、速查參數表、只談單一元件細節。
- **關鍵要素**：背景與挑戰、核心機制、為何這樣設計（取捨）、替代方案對比。
- **類比**：一篇談烹飪社會史的文章。

### Part 3: Engineering Governance

來源：工程治理實務，不屬於 Diataxis，獨立於四象限之外，用來隔離會污染四象限的內容。包含 decisions、testcases 兩個目錄。

分類原則：現況與歷史分離。explanation 描述系統「現在」如何運作；歷史決策進 decisions/。測試細節進 testcases/，不進 guides。

#### decisions
- **Purpose**：決策歷史日誌，以 ADR 格式撰寫；追加式、不可變、帶時間戳。
- **Must**：記錄當時背景、評估過的替代方案與後果；舊 ADR 不改原文，只標記 Outdated 並註明由哪個 ADR 取代（如 `Outdated: replaced by ADR-0012`）；每份 ADR 自足，不讀其他文件也看得懂決策的來龍去脈（為自足而保留與 reference 重複的 Context 是可接受的例外）。
- **Must Not**：描述系統現況（那是 explanation）。
- **關鍵要素**：狀態、背景、決策、結果評估（正負面影響）。
- 從舊文件拆出 ADR 時的狀態與改寫規則，見 [references/migration-acceptance.md](references/migration-acceptance.md) 第 5 節。

#### testcases
- **Purpose**：系統行為的客觀驗收契約，服務 QA、CI 與核心開發者。
- **Must**：邊界案例、異常斷言、覆蓋矩陣皆留在此；覆蓋矩陣（需求或不變式對應到案例）與各案例自己標註的對應需求（如 Covers 欄位）雙向一致；案例有穩定 ID。
- **Must Not**：教使用者操作。「如何執行測試」屬 guides；「輸入輸出型別」屬 reference。
- **關鍵要素**：前置條件、輸入邊界、預期斷言行為。
- 若測試程式或 CI 會解析文件格式，改動結構前要同步解析端，見 [references/migration-acceptance.md](references/migration-acceptance.md) 第 6 節。

## Validation Process

### 模式

- **Audit**：只有現成的文件，審查歸屬、粒度、內容要素與可用性。
- **Migration**：有來源文件（如單一大檔被拆成多份文件），除 Audit 的檢查外，必須加做「來源保真」與「反向可追溯」。細則見 [references/migration-acceptance.md](references/migration-acceptance.md)；實作者交接與多輪審查見 [references/review-protocol.md](references/review-protocol.md)。

### 步驟

1. **Identify & Granularity**：判定每份文件的類型與粒度。無法歸類或橫跨兩類者標記為混雜並建議拆分；多份同類型文件內容過少、零散且業務邏輯緊密相依，標記過度碎片化並建議合併；合併後過長或多主題者標記過度合併。
2. **Validate boundaries**：對照 Document Types 的 Must / Must Not 檢查內容污染。
3. **Validate content elements**：檢查內容是否涵蓋該類型的關鍵要素。不要求固定的章節結構、標題或順序；只有缺漏會讓讀者無法完成該類型的任務時，才算缺漏。文件 front matter 有宣告 metadata（性質、要求等級、權威、約束力）時，另依 [references/doc-metadata.md](references/doc-metadata.md) 檢查宣告與內容是否一致；未宣告則略過，不扣分。
4. **Mechanical checks**：能用工具的用工具，不靠肉眼目測；項目與輸出格式見 [references/mechanical-checks.md](references/mechanical-checks.md)。無法機械化的項目（如重複事實）由審查者判斷，並標明是判斷而非工具結果。
5. **Source fidelity（僅 Migration）**：逐段對照來源與新文件，不要求逐字，但每段內容都要能找到去處；只在來源出現一次的規則最容易遺失，要特別對照。同時檢查新文件有沒有來源沒有的推論、目的句或規則，不因「看起來合理」放行。分類標準、「找得到」的判斷、反向可追溯與逐區塊比較見 [references/migration-acceptance.md](references/migration-acceptance.md)。
6. **Reader walkthrough**：找沒參與撰寫、也沒看過來源（Migration）的讀者，只靠被審查的文件完成 5–7 個代表性任務，涵蓋專案實際提供的閱讀路徑。審查者讀過來源，不可充當讀者；讀者由使用者提供，或由審查者派出全新 context 的 subagent。此步通常找到最多問題，不可用靜態檢查取代。任務設計、隔離、計數與回報格式見 [references/reader-walkthrough.md](references/reader-walkthrough.md)；取不到讀者時的判定見 [references/scoring-calibration.md](references/scoring-calibration.md)。
7. **Executable content**：文件內的程式碼、指令、設定範例要在不改動被驗證專案的隔離環境中實際執行；做法見 [references/mechanical-checks.md](references/mechanical-checks.md)。走查只讀不跑，不得宣稱範例「可用」。
8. **Report**：依「輸出格式」回報違規。

審查整個 docs/ 時，先檢查 intent-doc 與目錄結構，評估整體粒度，再逐份檢查文件。多輪或多審查者時，遵守 [references/review-protocol.md](references/review-protocol.md)。

### 污染搬移對照

| 發現 | 搬至 |
|---|---|
| tutorials 含架構原理 | explanation |
| guides 含全量配置清單 | reference |
| guides 含大量測試斷言 | testcases |
| testcases 含「如何執行測試」教學 | guides |
| reference 含操作教學 | guides |
| reference 含心得或建議 | explanation |
| explanation 含操作步驟 | tutorials 或 guides |
| explanation 含過期歷史 | decisions |
| ADR 描述現況 | 改寫進 explanation，ADR 保持歷史原貌 |
| 同一事實完整出現在多處 | 保留在權威來源（SSOT），其餘改連結 |

## Validation Checklist

逐項檢查；每項出現問題時，依「裁量」評估對讀者的實際影響來決定扣分，不是出現即不合格。唯一的硬規則見文件開頭。

- [ ] 每份文件只屬於一個類型，無跨類型污染，且沒有把行為前提誤當設計理由移走
- [ ] 粒度適中：無多職責過載、無過度碎片化、無過度合併
- [ ] 符合 SSOT：每個事實只有一個權威來源，其餘為連結
- [ ] 內容涵蓋各類型的關鍵要素，Cross-link 符合各類型 Must
- [ ] 機械檢查通過：無死連結、壞錨點、自我連結、舊檔名殘留；新文件皆有入站連結且從導覽找得到；橫切主題有索引入口
- [ ] 讀者走查：代表任務皆能完成；做不到時已列為驗證缺口
- [ ] Migration：省略清單無「其他」類項目（硬規則）；新增內容皆可追溯或已登記授權；無未解決的「更差」區塊（硬規則）
- [ ] 類型名實相符：檔案自述性質與所在類型一致，不符者已改名、移動或標示
- [ ] 僅在文件有宣告 metadata 時適用：宣告與內容一致（見 [references/doc-metadata.md](references/doc-metadata.md)）
- [ ] 外部引用（程式註解、README、CI 解析）的路徑與格式仍有效；文件內的可執行內容已在隔離環境驗證
- [ ] intent-doc 符合「必備」兩項；README 保持精簡
- [ ] 目錄與檔名風格一致（`README.md`、ADR 編號等通行慣例除外）

## Confidence Score

審查結尾給一個 0-100% 的「信心指數」，代表審查者有多大把握認為這份文件（或體系）可以直接交付給讀者使用。**預設 90% 以上合格**；使用者指定其他門檻（如 95%）時以使用者為準，並在報告中註明。

這是質化判斷，不是把 Checklist 勾選數或扣分表換算成百分比。讀完全部內容後，以讀者視角整體評估：讀者能否在對的地方找到需要的東西、是否會被錯放的內容誤導或卡住。一項嚴重違規（例如 tutorials 無法照做、reference 有錯誤規格、內容遺失）可以讓分數低於門檻，即使其他項目全數通過；數個無傷大雅的小瑕疵也可能仍維持合格。

**分軸評分**：Migration 模式下，「內容保真」與「讀者可用性」分開打分並各自給理由；兩軸都要各自達標，整體才算合格，不取平均。兩軸可能差很大（例如保真高、可用性低），合併成單一分數會藏住真正的問題。Audit 模式只評可用性軸。各軸錨點、驗證覆蓋率上限與報告寫法見 [references/scoring-calibration.md](references/scoring-calibration.md)。

**錨點參考**

| 信心指數 | 意義 |
|---|---|
| 95-100% | 邊界、結構、連結皆乾淨，完全確信可交付 |
| 90-94% | 僅有不影響讀者使用的微小瑕疵 |
| 70-89% | 大致可用，但有明確的邊界污染或缺漏，需修正後重審 |
| 40-69% | 多處職責混雜，或導航嚴重缺失導致讀者找不到入口 |
| 0-39% | 結構性問題，幾乎需要重寫 |

錨點只描述各分數區間的意義；合格與否一律以當次門檻判定。

**評分規則**
- 附上 2-4 句理由，說明為什麼是這個分數、最拉低分數的是什麼；每個扣分都要附證據（檔案與具體現象）。
- 扣分歸因，分三類：
  - A 類：需要使用者或作者決策、審查者無權自行補的缺口。Migration 中通常是來源本身就沒有或有歧義；Audit 中如缺少只有作者才知道的專案資訊。證據要求見 [references/review-protocol.md](references/review-protocol.md)。
  - B 類：可以修正的問題。預期分數的寫法見 [references/scoring-calibration.md](references/scoring-calibration.md)，執行者標註見 review-protocol.md。
  - C 類：框架下的合理取捨（例如刻意保留的重複 Context），不必修。
- 未達門檻時：列出「差幾分」與「升到合格所需的最少修正」，優先列 B 類中最划算的。A 類單獨列為「需決策」，不計入修正。
- 資訊不足時（例如只拿到部分文件）不要硬給高分；說明受限範圍，並依已見內容保守評分。無法做讀者走查是特例，判定為「未能判定」，見 [references/scoring-calibration.md](references/scoring-calibration.md)。
- 修正後重審時重新評分，不沿用舊分數。

## 輸出格式

審查報告固定使用以下結構。重審時改用 [references/review-protocol.md](references/review-protocol.md) 的重審模板。

```markdown
# 文件審查報告
## 摘要（整體符合度與最嚴重的 3 個問題）
## 修正待辦（B 類，依預期可收回分數由高到低）
## 違規清單
| 編號 | 檔案 | 判定類型 | 違規 | 類別 A/B/C | 預期分數 | 建議動作（搬移 / 拆分 / 合併 / 刪除） | 驗收條件 |
## 機械檢查結果（死連結 / 自我連結 / 孤兒檔 / 重複事實 / ID 一致；各項標明驗證覆蓋率：全量工具 / 抽樣）
## 讀者走查結果（任務、必要檔數、跳轉次數、卡點類別、是否完成；讀者事前已知與隔離稽核結果）
## 驗證缺口（未能執行的驗證與對判定的影響；無則省略）
## 來源保真與逐區塊比較（僅 Migration：省略清單、反向可追溯、合併結果表）
## Cross-link 缺漏
## Checklist 結果（含一行 Metadata 檢查：已啟用 / 未宣告略過）
## 信心指數（0-100% ± 範圍，門檻預設 90%）
- 分數與判定（合格 / 不合格 / 未能判定）；Migration 分軸列出
- 理由（2-4 句，扣分附證據）
- 扣分歸因（A 需決策 / B 可修 / C 合理取捨）
- 未達門檻時：差幾分與升到合格所需的最少修正
```

**範例**
Input：`docs/guides/deploy.md` 內含 40 行完整 config 鍵值表與一段 2019 年改用 etcd 的原因。
Output：R1：全量配置表屬 reference，搬至 `reference/config.md` 並於 guide 連結；R2：etcd 選型歷史屬 decisions，新增 ADR 並由 explanation 連結。信心指數 78%（不合格）：兩項污染都會讓讀者在任務中途被打斷，但步驟本身正確；完成上述兩項搬移後預期可達合格。扣分歸因：兩項皆 B 類，各約 +6 至 +7，均由實作者修。
