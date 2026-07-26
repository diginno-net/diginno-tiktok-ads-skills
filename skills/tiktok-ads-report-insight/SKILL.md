---
name: tiktok-ads-report-insight
description: "Use when the user asks for TikTok Ads insight, performance report, spend report, campaign/ad/adgroup breakdown, daily trend, CTR/CPC/CPM/video view/conversion analysis, or 'báo cáo ads' from official TikTok Ads MCP."
metadata:
  category: marketing-content
  subcategory: paid-ads
  source: diginno-tiktok-ads-skills
---

# TikTok Ads Report Insight

Generate read-only performance insight from official TikTok Ads MCP data.

## Required flow

1. Use `tiktok-ads-official` connection flow first.
2. If the user does not specify a date window, default to the last 30 account-timezone days and state the assumption.
3. Read advertiser info for timezone/currency/status.
4. Read campaign list with names and statuses.
5. Run `mcp__tiktok_ads.report_integrated_get`:
   - campaign level: `data_level=AUCTION_CAMPAIGN`, dimension `campaign_id`
   - daily trend: `data_level=AUCTION_ADVERTISER`, dimension `stat_time_day`
   - ad level when creative/ad signals matter: `data_level=AUCTION_AD`, dimension `ad_id`
6. Map returned IDs back to campaign/ad names using `campaign_get` and `ad_get`.
7. Summarize totals, winners, weak spots, and missing evidence.

## Default metrics

Use the metrics in `references/report-fields.md`.

## Output

Answer in Vietnamese:

- account/date/currency/timezone
- total table
- campaign breakdown
- ad-level notable signals
- daily concentration
- observations
- diagnoses with confidence
- recommended next reads/actions
- missing data

## Boundaries

- Do not mutate anything.
- Do not infer business performance from video views alone.
- Do not call zero conversion a tracking failure unless Pixel/event evidence supports it.
- Do not compare against generic benchmarks without objective, geo, audience, market, sample size, and source.
