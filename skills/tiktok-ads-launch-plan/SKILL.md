---
name: tiktok-ads-launch-plan
description: "Use to draft TikTok Ads campaign/adgroup/ad launch or change plans, including objective, budget, pixel placement, Spark Ads, carousel/video format, CTA, identity, and write-safety gate. Does not execute writes without explicit approval."
metadata:
  category: marketing-content
  subcategory: paid-ads
  source: diginno-tiktok-ads-skills
---

# TikTok Ads Launch Plan

Draft safe TikTok Ads changes. Do not execute write tools until the user approves the exact mutation.

## Planning flow

1. Use `tiktok-ads-official` to confirm advertiser and readable current state.
2. Collect:
   - campaign goal
   - product/service
   - destination
   - geography/language
   - budget and currency
   - creative assets
   - conversion definition
   - tracking/pixel/event source
3. Choose objective and optimization goal.
4. Check TikTok validity rules in `references/tiktok-validity-rules.md`.
5. Draft:
   - campaign
   - ad group
   - ad/creative
   - tracking
   - budget/pacing
   - naming convention
   - QA checklist
6. Present mutation plan using `references/mutation-plan-template.md`.

## Hard rules

- Pixel placement depends on objective; check the reference before proposing adgroup/ad tracking fields.
- TikTok in-feed does not support a single static image ad. Use video, Spark Ad, or carousel.
- Campaign creation/change must be paused or controlled by explicit launch approval.
- Do not invent advertiser, identity, pixel, app, product, or shop IDs.
