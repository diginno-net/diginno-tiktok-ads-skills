# TikTok Ads Report Metrics Reference

Use this as an operator checklist, not as exhaustive API documentation.

## Core scope

Always state:

- `advertiser_id`
- account name
- timezone
- currency
- date window
- report type
- data level
- dimensions
- metrics

## Common dimensions

- `stat_time_day`
- `campaign_id`
- `adgroup_id`
- `ad_id`
- `country_code`

## Common metrics

- `spend`
- `impressions`
- `clicks`
- `ctr`
- `cpc`
- `cpm`
- `conversion`
- `cost_per_conversion`
- `video_play_actions`
- `video_watched_2s`
- `video_watched_6s`
- `average_video_play`

## Derived ratios

Calculate only when denominator is non-zero:

- 2s watch rate = `video_watched_2s / impressions`
- 6s watch rate = `video_watched_6s / impressions`
- click share = campaign/ad clicks divided by total clicks
- spend share = campaign/ad spend divided by total spend

## Interpretation boundaries

- Objective `VIDEO_VIEWS` can make view metrics look good while click/conversion intent is weak.
- CTR near zero on video view campaigns is not automatically failure; judge against business goal.
- Zero conversion can mean objective mismatch, missing tracking, low sample size, conversion lag, or actual poor performance. Do not pick one without evidence.
- Same-day data can be unstable.
- TTAM downloaded reports may differ from synchronous API reports; use async reports when exact TTAM parity matters.
