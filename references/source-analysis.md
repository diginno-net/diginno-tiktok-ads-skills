# Source Analysis

Date: 2026-07-26

## What was useful

### `claude-ads`

Best source for skill design discipline:

- clear separation between audit, report, launch, optimize, creative, attribution, budget
- evidence-first reporting
- strong mutation gate
- avoids universal paid-media rules
- separates observation, diagnosis, recommendation, and proposed action

Used as conceptual inspiration for this repo's skill split.

### `ads-mcp`

Best source for packaging patterns:

- marketplace-style README
- install/sync scripts
- platform-specific skills plus shared MCP orchestration ideas
- TikTok-specific validity reminders around objective, pixel placement, budgets, CTA values

Used as structural inspiration, not as an active dependency.

### `tiktok-ads-cli`

Best source for TikTok Ads API taxonomy:

- advertiser
- campaign
- adgroup
- ad
- creative
- audiences
- report/reporting

Used to shape the official MCP tool map and report workflows.

### `tiktok-ads-mcp-server` and `tiktok-ads-mcp`

Useful mainly for understanding endpoint grouping and error boundaries. Not used as runtime because Codex already connects to the official TikTok MCP.

### `agent-skills-hub`

Broad skill examples are useful for naming/style review, but TikTok Ads API content should be treated as stale unless checked against official MCP schemas.

## Deliberate changes

- Replaced custom/local MCP assumptions with official `mcp__tiktok_ads` namespace.
- Removed token/app-secret setup from skill instructions.
- Made write actions draft-only until explicit approval.
- Added account discovery as mandatory first step.
- Added Vietnamese output shape for Diginno operator workflow.
