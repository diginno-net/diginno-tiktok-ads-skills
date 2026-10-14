#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Xuất bảng 7 ngày (mỗi video/ad một dòng) từ TikTok Ads sang CSV đúng cột bảng Lark.

Cần CLI `tiktok-ads-mcp` đã login (xem cli/tiktok-ads-mcp trong repo này).

Ví dụ:
  python3 scripts/export-7-ngay-csv.py \
      --advertiser-id <ADVERTISER_ID> \
      --start 2026-10-06 --end 2026-10-13 \
      --channel "<ten-kenh>" \
      --out reports/private/bang-7-ngay-2026-10-06_2026-10-13.csv

Lưu ý dữ liệu thật của khách: luôn ghi vào reports/private/ (đã gitignore),
không commit CSV vào git.
"""

import argparse
import csv
import json
import subprocess
import sys

COLUMNS = [
    "Ngày", "Kênh", "Tên video", "Link video", "Lượt xem", "Thích", "Yêu thích",
    "Comment", "Chia sẻ", "Follow", "Đơn", "Tiền quảng cáo", "ID quảng cáo",
    "Nguồn số", "Ô chưa có số", "Quyết định", "Vì sao", "Đã hỏi AI",
    "Đã được xem", "Người điền", "(tham chiếu) Mã bài TikTok",
]
MISSING = "Link, Yêu thích, Follow, Đơn, Quyết định, Vì sao"


def call(tool: str, params: dict) -> dict:
    proc = subprocess.run(
        ["tiktok-ads-mcp", "call", tool, "--params", json.dumps(params)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        sys.exit(f"Lỗi gọi {tool}: {(proc.stderr or proc.stdout).strip()[:300]}")
    data = json.loads(proc.stdout)
    if data.get("code") != 0:
        sys.exit(f"{tool} trả code={data.get('code')}: {data.get('message')}")
    return data.get("data", {})


def main() -> None:
    ap = argparse.ArgumentParser(description="Xuất bảng 7 ngày TikTok Ads ra CSV")
    ap.add_argument("--advertiser-id", required=True)
    ap.add_argument("--start", required=True, help="YYYY-MM-DD")
    ap.add_argument("--end", required=True, help="YYYY-MM-DD")
    ap.add_argument("--channel", required=True, help="Tên kênh ghi vào cột Kênh")
    ap.add_argument("--out", required=True, help="Đường dẫn CSV (nên đặt trong reports/private/)")
    args = ap.parse_args()

    report = call("report_integrated_get", {
        "advertiser_id": args.advertiser_id,
        "report_type": "BASIC",
        "data_level": "AUCTION_AD",
        "dimensions": ["ad_id"],
        "metrics": ["spend", "video_play_actions", "likes", "comments", "shares"],
        "start_date": args.start,
        "end_date": args.end,
        "page_size": 1000,
    })
    rows = [r for r in report.get("list", []) if float(r["metrics"].get("spend") or 0) > 0]
    rows.sort(key=lambda r: -float(r["metrics"]["spend"]))
    if not rows:
        sys.exit("Không có ad nào chi tiêu trong kỳ — kiểm tra lại advertiser/ngày.")

    # Lấy tên ad + mã bài TikTok (tối đa 40 id mỗi lần)
    ids = [r["dimensions"]["ad_id"] for r in rows]
    info = {}
    for i in range(0, len(ids), 40):
        data = call("ad_get", {
            "advertiser_id": args.advertiser_id,
            "filtering": {"ad_ids": ids[i:i + 40]},
            "fields": ["ad_id", "ad_name", "tiktok_item_id"],
            "page_size": 100,
        })
        for ad in data.get("list", []):
            info[ad["ad_id"]] = ad

    def num(metrics: dict, key: str) -> int:
        return int(float(metrics.get(key) or 0))

    with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        for r in rows:
            m, aid = r["metrics"], r["dimensions"]["ad_id"]
            ad = info.get(aid, {})
            writer.writerow([
                "", args.channel, ad.get("ad_name", ""), "", num(m, "video_play_actions"),
                num(m, "likes"), "", num(m, "comments"), num(m, "shares"), "",
                "", num(m, "spend"), aid, "TikTok Ads", MISSING,
                "", "", "", "", "", ad.get("tiktok_item_id") or "",
            ])
    print(f"Đã ghi {len(rows)} dòng vào {args.out}")


if __name__ == "__main__":
    main()
