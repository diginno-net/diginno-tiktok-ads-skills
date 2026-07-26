# Official TikTok Ads MCP Tool Map

Use fully qualified tool names from the `mcp__tiktok_ads` namespace.

## Connection and account discovery

Read-only:

- `mcp__tiktok_ads.user_info_get`: verify OAuth and current TikTok Business user.
- `mcp__tiktok_ads.auth_advertiser_get`: list authorized advertiser accounts.
- `mcp__tiktok_ads.advertiser_info_get`: retrieve account status, timezone, currency, country, role.

Always start here before campaign, report, Pixel, Shop, or audience calls.

## Core hierarchy

```text
Advertiser
  -> Campaign
    -> Ad Group
      -> Ad
        -> Creative / Identity / Asset
```

Read-only:

- `mcp__tiktok_ads.campaign_get`
- `mcp__tiktok_ads.adgroup_get`
- `mcp__tiktok_ads.ad_get`
- `mcp__tiktok_ads.smart_plus_ad_get`

## Reporting

Preferred:

- `mcp__tiktok_ads.report_integrated_get` for synchronous report reads.
- `mcp__tiktok_ads.report_task_create` only when asynchronous report parity/export is required.
- `mcp__tiktok_ads.report_ad_benchmark_get` only after verifying the object accumulated enough impressions for the benchmark endpoint.

Common reporting parameters:

- `advertiser_id`
- `report_type`
- `data_level`
- `dimensions`
- `metrics`
- `start_date`
- `end_date`
- `timezone` and `currency` from advertiser info

## Measurement, Pixel, Events

Use Pixel/event source tools if exposed in the active MCP namespace. Do not claim tracking is healthy from campaign performance alone.

## Commerce

When available:

- `mcp__tiktok_ads.store_list_get`
- `mcp__tiktok_ads.store_product_get`
- `mcp__tiktok_ads.gmv_max_store_list_get`
- `mcp__tiktok_ads.gmv_max_report_get`

Treat unavailable or ineligible Shop/GMV Max features as unscored opportunities.

## Write-capable tools

Any create/update/delete/status/assign/unassign/post/appeal tool is write-capable. Use `references/mutation-gate.md` from the repo before any write.
