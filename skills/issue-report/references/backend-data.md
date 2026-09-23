# 後端服務 / 資料管線 issue

## Environment

後端的「環境」不是作業系統版本，而是足以重建出問題當下狀態的座標。只列與本問題相關的項目——整頁 config dump 會稀釋掉真正重要的那兩行。

服務類：
- service 名稱與 version / image tag / commit SHA
- 環境（prod / staging / dev）、region、cluster
- endpoint 或 RPC method
- 上下游相依服務，含第三方
- 相關 feature flag 或 config 的最近變更時間

資料管線類：
- job / DAG / pipeline 名稱與 run ID
- 來源與目標全名（table、topic、bucket path）
- 受影響的 partition 或時間區間，標明時區
- 執行引擎與版本（Flink、Spark、BigQuery job）
- schema version 或最近一次 schema 變更時間

## Steps to Reproduce

後端問題多半是「送某種請求」或「跑某個 job」，能貼指令就貼指令，比文字描述精確得多。敏感值（token、金鑰、真實使用者 ID）要遮罩。

```bash
curl -X POST https://api.example.com/v1/sessions \
  -H 'Content-Type: application/json' \
  -d '{"device_type":"ctv","ad_pod_duration":120}'
# → 504 after ~30s
```

```sql
SELECT COUNT(*) FROM `project.dataset.daily_impression`
WHERE partition_date = '2026-09-21' AND source = 'lg_channels';
-- → 0，前七天皆為 ~1.2M
```

## 資料正確性問題的額外欄位

資料問題比服務問題更難判斷「到底壞了沒」，所以要把判斷依據寫出來：

- **異常的量化描述**：缺多少筆、差多少百分比
- **比對基準**：前一天、上游來源系統、另一條驗證路徑
- **首次出現時間**：往回追到哪一天還是正常的
- **下游取用者**：哪些報表、模型、對外 API 吃這份資料
- **資料是否已外流**：已進到報表或已回報給客戶的資料，修復不只是 backfill，還要對外更正，成本差一個量級

## Impact

「影響很大」無法排序，給數字或範圍：錯誤率、受影響請求比例、partition 數與資料筆數、是否影響營收路徑（計費、對帳）、有無 workaround 及其成本。

## 範例

~~~markdown
# daily_ad_impression 缺少 lg_channels 來源資料（2026-09-21 partition）

## Summary
2026-09-21 的 `daily_ad_impression` partition 中，`source = 'lg_channels'` 筆數為 0，
前七天平均約 1.2M 筆。該表為每日 ad revenue 對帳的上游，已導致 09-22 報表低估。

## Environment
- Pipeline：`ad-impression-daily`（Flink 1.18），run ID `run-20260922-0300`
- 來源：GCS `gs://example-ssai-raw/lg/2026/09/21/`
- 目標：`example-ads.mart.daily_ad_impression`，partition `2026-09-21`（UTC+8）
- 09-19 曾調整過 source path 的 prefix 規則

## Observations
- **發生時間**：2026-09-22 03:00 CST 的排程 run
- **發生頻率**：目前僅此一次，09-20 以前正常
- **定位線索**：job 狀態為 SUCCESS 且無 error log；來源路徑下確認有 214 個檔案
- **共同條件**：僅 `lg_channels` 受影響，其他 source 筆數正常

## Expected vs Actual
- **Expected**：`source = 'lg_channels'` 約 1.2M 筆
- **Actual**：0 筆，且 job 未報錯

## Impact
- 09-22 ad revenue 對帳報表低估，已被下游 BI dashboard 取用
- 下游 CTR scoring model 當日 training data 缺一個 source
- 資料已外流至報表，修復需 backfill 並對外更正

## Evidence
```
03:00:12 INFO  source path resolved: gs://example-ssai-raw/lg/2026/09/21/*.parquet
03:04:51 INFO  records written: 0
03:04:51 INFO  job finished: SUCCESS
```

## Severity / Priority
- **Severity**：Major — 資料靜默缺失且 job 回報成功，無告警攔截
- **Priority**：High — 已影響對帳數字，且靜默失敗模式可能重複發生
~~~
