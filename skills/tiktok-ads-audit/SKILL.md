---
name: tiktok-ads-audit
description: "Use for TikTok Ads account health audit, campaign diagnostics, tracking audit, budget/pacing check, objective mismatch analysis, Pixel/Event API review, policy risk, or prioritized TikTok Ads opportunities."
metadata:
  category: marketing-content
  subcategory: paid-ads
  source: diginno-tiktok-ads-skills
---

# TikTok Ads Audit

Run a source-grounded TikTok Ads audit from official MCP reads and user-supplied business context.

## Procedure

1. Use `tiktok-ads-official` connection and advertiser discovery first.
2. Collect business context:
   - product/service
   - funnel goal
   - conversion definition
   - economics/margin if available
   - geography
   - date window
   - landing destination
3. Build an account snapshot:
   - advertiser status/currency/timezone
   - campaign/adgroup/ad hierarchy
   - campaign objectives and statuses
   - spend/performance report
   - Pixel/event/tracking evidence if available
4. Evaluate:
   - objective and funnel fit
   - measurement and conversion evidence
   - creative signal
   - budget and pacing
   - campaign structure
   - audience/placement if readable
   - Shop/GMV Max eligibility if relevant
   - policy or approval status
5. Classify each finding:
   - observation
   - diagnosis
   - recommendation
   - missing input
   - unscored opportunity
6. Produce prioritized next steps with owner, effort, expected effect, and verification metric.

## Evidence coverage

Use these statuses:

- `complete`: hierarchy, spend, objective, tracking, and relevant creative evidence are available.
- `provisional`: enough performance data exists, but tracking/creative/business context is incomplete.
- `partial`: MCP access works but key account objects or reports are missing.
- `insufficient_evidence`: too little spend/data/context to score.

## Boundaries

- Optional or beta features do not reduce account health score.
- Do not issue universal pause/budget/bid rules.
- Proposed changes stay as drafts until mutation gate approval.
