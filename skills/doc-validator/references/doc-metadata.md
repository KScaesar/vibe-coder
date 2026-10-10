# 文件 metadata（可選）

這份文件定義 `SKILL.md` 步驟 3 引用的可選檢查。文件在 front matter 宣告自己的性質、要求等級、來源權威與法律效力，審查者據此檢查「宣告與內容是否一致」。

## 原則

- **全部可選**：沒有宣告的欄位不檢查、不扣分。不得因文件沒寫 metadata 而建議補上，除非使用者要求。
- **只查宣告與內容是否一致**：不評斷文件「應該」是什麼性質。
- **全部歸「裁量」**：不新增硬規則；依對讀者的實際影響決定扣分。
- **與四象限正交**：metadata 描述文件的規範屬性，不取代 tutorials / guides / reference / explanation 的歸類。

## 宣告格式

寫在被審查文件最上方的 YAML front matter，四個欄位皆可單獨出現：

```yaml
---
doc-class: normative
requirement-language: rfc8174
authority: authoritative
binding: non-binding
---
```

## 欄位

### doc-class：文件性質（Document Classification）

說明：
- 描述文件內容的角色與用途。
- 區分規範內容與說明內容。

術語（即宣告值）：
- `normative`
- `informative`
- `non-normative`

來源：
- W3C Specification Guidelines

如何區分：
- `normative`：內容定義「必須遵守什麼」，讀者照做才算符合。
- `informative`：整份文件只提供背景、範例、說明，不定義遵守義務。
- `non-normative`：`normative` 文件中的說明段落（註記、範例、背景），用於標示「這一段不構成要求」。
- 判斷方式：拿掉這段，符合性的判定標準會不會改變？會，是 `normative`；不會，是 `informative` 或 `non-normative`。

檢查：
- `normative`：要求語句中有無未定義強度的模糊詞（應該、需要、最好）。模糊詞讓讀者無法判斷是否必須遵守時才扣分。
- `informative`：有無 MUST / MUST NOT 等規範語句。有則不符：改標 `normative`，或把規範語句移到 `normative` 文件。
  - 例外：明確標示為引用、範例的規範語句不算。
- `non-normative`：標示為非規範的段落內有無規範語句，有則矛盾。

### requirement-language：要求等級（Requirement Level）

說明：
- 描述規範要求的強度與遵守程度。

術語（文件中使用的關鍵字，一律大寫）：
- `MUST`
- `MUST NOT`
- `SHOULD`
- `SHOULD NOT`
- `MAY`

來源：
- RFC 8174

宣告值：
- `rfc8174`：全文以上述關鍵字表達要求等級，且僅「全大寫」時有規範意義（RFC 8174）。

如何區分：
- `MUST` / `MUST NOT`：沒做到就是不符合。
- `SHOULD` / `SHOULD NOT`：有正當理由才可不照做，且需理解後果。
- `MAY`：做或不做皆符合。
- 小寫的 must、should 只是一般語句，不計入規範。

檢查：
- 要求語句是否使用上述大寫關鍵字。
- 小寫 must / should 出現在要求語句中，視為強度不明。混用造成歧義時才扣分。

### authority：來源權威（Source Authority）

說明：
- 描述衝突時應優先採用的依據來源。

術語（即宣告值）：
- `authoritative`

來源：
- Technical Specification Governance Practice

如何區分：
- 宣告 `authoritative` 表示：這份文件與其他文件對同一事實說法不同時，以這份為準。
- 沒有宣告不代表較低權威，只代表本文件未主張。

檢查：
- 其他文件有無對同一事實給出矛盾說法。有則歸 SSOT 違規。
- 兩份文件同時宣告 `authoritative` 且內容衝突：另列「需決策」（A 類），審查者不自行裁定誰為準。

### binding：法律效力（Legal Binding）

說明：
- 描述文件是否具有法律、契約或制度上的拘束力。

術語（即宣告值）：
- `binding`
- `non-binding`

來源：
- Legal / Contract Documentation Practice

如何區分：
- `binding`：違反會產生契約、法律或制度上的後果（如 SLA、合約、合規制度）。
- `non-binding`：參考、建議或內部慣例，違反不產生上述後果。
- 與 `doc-class` 無關：`normative` 文件不一定是 `binding`（如開源專案的編碼規範）。

檢查：
- `binding`：有無版本、生效日、變更程序。缺漏才扣分；條款內容是否合法不在審查範圍。
- `non-binding`：有無「必須遵守」「違反即」等具約束語氣。語氣與宣告矛盾時列出。

## 與文件類型的對應

建議預設值，供作者宣告時參考；審查者不得用它反推「缺少宣告」或「宣告不符類型」：
- reference、testcases：常見 `normative`、`authoritative`。
- decisions：常見 `informative`（歷史紀錄）。
- explanation、tutorials、guides：常見 `informative`。

## 例外處理

- 欄位值不在上列範圍（如 `doc-class: draft`）：列為「宣告無法識別」，不推測意圖。

## 報告寫法

在「Checklist 結果」內加一行，不另開章節：
- 有任何文件宣告：`Metadata 檢查：已啟用（N 份文件宣告）`，違規併入違規清單，判定類型欄填「metadata」。
- 全部未宣告：`Metadata 檢查：未宣告，略過`。
