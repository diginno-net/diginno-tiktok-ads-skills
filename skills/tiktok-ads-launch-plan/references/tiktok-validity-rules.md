# TikTok Validity Rules

Operational reminders from OSS review and TikTok API behavior. Verify against active official MCP schemas before write.

## Pixel placement

- Conversion-oriented objectives such as `CONVERSIONS`, `WEB_CONVERSIONS`, `PRODUCT_SALES`, `SHOP_PURCHASES`: pixel belongs on the ad group and optimization event is required.
- Non-conversion objectives: tracking pixel generally belongs on the ad, not the ad group.

If unclear, stop and verify with official tool schema/documentation before proposing write parameters.

## Creative format

TikTok in-feed does not support one static single-image ad. Offer:

- video ad
- Spark Ad
- carousel with 2-10 images plus music

## CTA

Avoid invalid CTA aliases. Prefer explicit supported CTA values such as:

- `LEARN_MORE`
- `SHOP_NOW`
- `DOWNLOAD_NOW`
- `SIGN_UP`
- `GET_QUOTE`
- `BOOK_NOW`
- `INSTALL_NOW`

## Budget

Budget floors depend on currency and account settings. Read account currency and current UI/API errors. Do not force a universal amount.
