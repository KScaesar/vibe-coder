# 文件 metadata

適用條件：被審查文件的 front matter 有宣告下列欄位時才讀。文件在 front matter 宣告自己的性質、要求等級、來源權威與法律效力，審查者據此檢查「宣告與內容是否一致」。

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

### doc-class：文件性質（來源：W3C Specification Guidelines）

| 值 | 意思 | 檢查 |
|---|---|---|
| `normative` | 定義「必須遵守什麼」，讀者照做才算符合。判斷：拿掉這段，符合性的判定標準會不會改變？會，就是 normative | 要求語句中有無未定義強度的模糊詞（應該、需要、最好）；讀者無法判斷是否必須遵守時才扣分 |
| `informative` | 只提供背景、範例、說明，不定義遵守義務 | 有 MUST / MUST NOT 等規範語句即不符：改標 `normative`，或把規範語句移到 normative 文件。明確標示為引用、範例者除外 |

### requirement-language：要求等級（來源：RFC 8174）

| 值 | 意思 | 檢查 |
|---|---|---|
| `rfc8174` | 以全大寫關鍵字表達要求等級：`MUST` / `MUST NOT` 沒做到就不符合；`SHOULD` / `SHOULD NOT` 有正當理由且理解後果才可不照做；`MAY` 做或不做皆符合。小寫 must、should 只是一般語句 | 要求語句是否使用大寫關鍵字；小寫 must / should 出現在要求語句中視為強度不明，混用造成歧義時才扣分 |

### authority：來源權威

| 值 | 意思 | 檢查 |
|---|---|---|
| `authoritative` | 與其他文件對同一事實說法不同時，以本文件為準。未宣告不代表權威較低，只代表本文件未主張 | 兩份文件同時宣告且內容衝突：A 類，審查者不自行裁定誰為準 |

### binding：法律效力

與 `doc-class` 無關：normative 文件不一定是 binding（如開源專案的編碼規範）。

| 值 | 意思 | 檢查 |
|---|---|---|
| `binding` | 違反會產生契約、法律或制度上的後果（如 SLA、合約、合規制度） | 有無版本、生效日、變更程序；缺漏才扣分。條款內容是否合法不在審查範圍 |
| `non-binding` | 參考、建議或內部慣例，違反不產生上述後果 | 有無「必須遵守」「違反即」等約束語氣；與宣告矛盾時列出 |

## 與文件類型的對應

建議預設值，供作者宣告時參考；審查者不得用它反推「缺少宣告」或「宣告不符類型」：
- reference、testcases：常見 `normative`、`authoritative`。
- decisions、explanation、tutorials、guides：常見 `informative`。

## 例外處理

欄位值不在上列範圍（如 `doc-class: draft`）：列為「宣告無法識別」，不推測意圖。

## 報告寫法

在「Checklist 結果」內加一行，不另開章節：
- 有任何文件宣告：`Metadata 檢查：已啟用（N 份文件宣告）`，違規併入違規清單，判定類型欄填「metadata」。
- 全部未宣告：`Metadata 檢查：未宣告，略過`。
