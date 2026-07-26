# Case Studies ứng dụng TikTok Ads MCP

Ngày viết: 2026-07-26

Tài liệu này mô tả các case study thực tế có thể triển khai bằng official TikTok Ads MCP trong Codex. Mục tiêu là biến MCP từ “tool đọc API” thành workflow vận hành ads có guardrail: đọc đúng account, phân tích có bằng chứng, đề xuất rõ ràng, và chỉ write khi có duyệt.

## Nguyên tắc chung

Mọi case nên đi qua flow tối thiểu:

1. Xác nhận OAuth bằng `mcp__tiktok_ads.user_info_get`.
2. Lấy advertiser được cấp quyền bằng `mcp__tiktok_ads.auth_advertiser_get`.
3. Đọc thông tin account bằng `mcp__tiktok_ads.advertiser_info_get`.
4. Đọc hierarchy bằng `campaign_get`, `adgroup_get`, `ad_get`.
5. Đọc report bằng `report_integrated_get`.
6. Tách rõ:
   - dữ liệu đã kiểm
   - quan sát
   - chẩn đoán
   - khuyến nghị
   - thiếu dữ liệu
   - kế hoạch write nếu có

Không lưu token, cookie, app secret, export raw nhạy cảm hoặc customer list vào repo/report.

## Case 1: Account access smoke test sau OAuth

### Bối cảnh

Khách hoặc team vừa cấp quyền Business Center/Advertiser cho user. Cần biết Codex đã nhìn thấy account ads chưa.

### MCP reads

- `user_info_get`
- `auth_advertiser_get`
- `advertiser_info_get`

### Output nên có

- user OAuth đã connect hay chưa
- danh sách advertiser ID/name
- role, status, timezone, currency
- quyền đọc account có đủ để tiếp tục audit/report hay không

### Giá trị vận hành

Giảm lỗi “đã join nhưng chưa thấy account” trước khi đi vào phân tích. Case này phù hợp làm bước đầu trong onboarding khách mới.

## Case 2: Báo cáo nhanh campaign performance

### Bối cảnh

Founder/Account muốn biết ads đang chạy có gì đáng chú ý mà không cần vào TikTok Ads Manager.

### MCP reads

- `campaign_get`
- `report_integrated_get` với:
  - `data_level=AUCTION_CAMPAIGN`
  - dimension `campaign_id`
  - metrics `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `cpm`, `conversion`, `cost_per_conversion`, `video_play_actions`, `video_watched_2s`, `video_watched_6s`, `average_video_play`

### Insight mẫu

- campaign nào tiêu nhiều nhất
- campaign nào có CTR/CPC tốt nhất
- campaign nào chỉ tạo view nhưng không tạo click/conversion
- campaign nào đang disabled nhưng vẫn cần học từ dữ liệu cũ

### Giá trị vận hành

Dùng cho weekly check, daily check, hoặc review nhanh trước cuộc họp khách.

## Case 3: Ad-level creative signal review

### Bối cảnh

Cùng một campaign có nhiều ad/video. Cần biết creative nào có tín hiệu tốt hơn trước khi sản xuất biến thể mới.

### MCP reads

- `report_integrated_get` với `data_level=AUCTION_AD`, dimension `ad_id`
- `ad_get` để map ad ID về tên campaign/adgroup/ad

### Metrics chính

- spend
- impressions
- clicks
- CTR
- CPC
- video plays
- 2s watched
- 6s watched
- average video play

### Chẩn đoán có thể đưa ra

- creative có hook tương đối tốt nếu 2s/6s watch rate cao hơn nhóm còn lại
- creative có intent tốt nếu CTR/click share cao hơn dù CPM không rẻ
- creative chỉ mua view rẻ nếu play volume cao nhưng click/conversion yếu

### Cảnh báo

Không kết luận “creative hay/dở” chỉ từ tên ad. Nếu không có video/screenshot/landing page, ghi rõ đây là review theo performance signal, chưa phải creative review đầy đủ.

## Case 4: Zero conversion diagnosis

### Bối cảnh

Report cho thấy spend có, impression/click có, nhưng conversion bằng 0.

### MCP reads

- `campaign_get` để xem objective
- `adgroup_get` để xem optimization/promotion/tracking fields nếu tool schema trả được
- `report_integrated_get` để kiểm tra conversion theo campaign/adgroup/ad/day
- Pixel/event source tools nếu official MCP namespace đang expose

### Các khả năng cần phân biệt

- objective đang là `VIDEO_VIEWS` hoặc traffic/view nên không tối ưu conversion
- Pixel/Event API chưa gắn hoặc không có event activity
- conversion definition không khớp funnel
- data window quá ngắn hoặc conversion lag chưa đủ
- spend/sample size quá thấp
- creative/landing page tạo intent thấp

### Output nên có

- không gọi zero conversion là tracking lỗi nếu chưa có bằng chứng Pixel/Event
- đưa danh sách kiểm tra tiếp theo
- nếu cần chuyển objective/tracking, chỉ lập mutation plan, chưa write

## Case 5: Budget and pacing review

### Bối cảnh

Khách hỏi “tiền tiêu có hiệu quả không”, “có nên tăng/ngắt ngân sách không”.

### MCP reads

- `campaign_get`
- daily `report_integrated_get` với dimension `stat_time_day`
- campaign/adgroup level report nếu cần breakdown

### Phân tích

- spend tập trung vào ngày nào
- CPM/CPC biến động theo ngày
- campaign nào chiếm spend share lớn nhưng signal yếu
- campaign nào tiêu ít nhưng click/video signal tốt

### Guardrail

Không dùng rule kiểu “CTR dưới X thì tắt” hoặc “CPA trên X thì giảm” nếu chưa có objective, margin, conversion lag, target CPA/ROAS và sample size.

### Output nên có

- đề xuất tăng/giảm/pause ở dạng draft
- mức độ tin cậy
- điều kiện verify sau thay đổi

## Case 6: Objective mismatch check

### Bối cảnh

Doanh nghiệp muốn lead/sale nhưng campaign đang chạy `VIDEO_VIEWS` hoặc engagement.

### MCP reads

- `campaign_get`
- report campaign/ad level
- tracking/Pixels nếu có

### Chẩn đoán

Nếu campaign objective không khớp funnel, report có thể đẹp ở view/CPM nhưng yếu ở click/conversion. MCP giúp chỉ ra mismatch bằng dữ liệu objective + performance.

### Hành động tiếp theo

- giữ campaign video view nếu mục tiêu là awareness
- tạo test campaign mới đúng objective nếu mục tiêu là lead/sale
- định nghĩa conversion event trước khi tối ưu conversion

## Case 7: Pre-launch QA cho campaign mới

### Bối cảnh

Team chuẩn bị tạo TikTok campaign từ Codex/MCP hoặc từ Ads Manager, cần checklist trước khi launch.

### MCP/user inputs

- advertiser ID
- identity/Spark authorization nếu dùng Spark Ads
- creative asset/video/carousel
- landing URL
- objective
- budget/currency
- geo/language
- pixel/event source

### QA checklist

- objective khớp funnel
- pixel placement đúng objective
- CTA hợp lệ
- creative format hợp lệ: video, Spark Ads, hoặc carousel; không dùng single static image in-feed
- budget không thấp hơn floor theo currency/account
- campaign tạo ở trạng thái paused hoặc launch có duyệt rõ

### Output nên có

Mutation plan với before/after, blast radius, rollback, verification window và câu hỏi duyệt rõ ràng.

## Case 8: TikTok Shop / GMV Max readiness

### Bối cảnh

Khách ecommerce muốn biết có thể dùng Shop Ads hoặc GMV Max không.

### MCP reads

- store/shop listing tools nếu namespace expose
- `gmv_max_store_list_get`
- `gmv_max_report_get`
- campaign/product/shop reads liên quan nếu có quyền

### Output nên có

- shop/store nào account nhìn thấy
- GMV Max có available hay không
- campaign/product nào đủ điều kiện
- nếu không thấy feature, ghi là unscored opportunity, không tính là lỗi account

### Giá trị vận hành

Tách rõ vấn đề “chưa đủ quyền/chưa available” với “setup sai”.

## Case 9: Creative production brief từ dữ liệu ads

### Bối cảnh

Sau khi có ad-level report, team content cần brief sản xuất video mới.

### MCP reads

- ad-level report
- `ad_get`
- creative/video metadata nếu namespace expose và có quyền

### Output brief

- creative đang thắng theo signal nào
- điểm cần giữ: hook/angle/offer/CTA nếu có bằng chứng
- điểm cần test: hook mới, proof mới, CTA mới, landing angle mới
- số lượng biến thể đề xuất
- metric success sau test

### Guardrail

Không public hóa creative/customer data nếu chưa có duyệt. Không biến ad text nội bộ thành example công khai.

## Case 10: Client-facing monthly TikTok Ads report

### Bối cảnh

Diginno cần xuất báo cáo định kỳ cho khách.

### MCP reads

- advertiser info
- campaign/adgroup/ad hierarchy
- campaign/ad/day reports
- optional tracking/shop/creative diagnostics nếu relevant

### Cấu trúc report

1. Executive summary.
2. Scope: account, date range, timezone, currency.
3. Total performance.
4. Campaign breakdown.
5. Creative/ad signal.
6. Tracking/conversion status.
7. Budget/pacing.
8. Recommendations.
9. Missing data and caveats.
10. Next measurement plan.

### Giá trị vận hành

Chuẩn hóa báo cáo khách mà vẫn giữ fact/diagnosis/recommendation riêng biệt. Phù hợp publish sang Lark Docs hoặc gửi khách sau khi sanitize.

## Case 11: Delivery anomaly monitor

### Bối cảnh

Campaign đang chạy nhưng đột ngột không tiêu tiền, CPM tăng mạnh, click tụt, hoặc ads bị disable/reject.

### MCP reads

- `campaign_get`
- `adgroup_get`
- `ad_get`
- daily/hourly `report_integrated_get` nếu date range cho phép

### Rule monitor an toàn

- status chuyển từ enable sang disable/reject
- spend hôm nay bằng 0 trong khi campaign expected active
- CPM/CPC biến động mạnh so với median gần đây
- impressions tụt mạnh

### Output nên có

- anomaly
- affected object IDs
- last normal period
- current state
- suggested read/check next
- không tự bật/tắt campaign nếu chưa duyệt

## Case 12: Account handover audit

### Bối cảnh

Diginno nhận lại account từ khách/agency cũ. Cần snapshot để bàn giao và xác định việc ưu tiên.

### MCP reads

- advertiser info
- all visible campaigns/adgroups/ads
- report 30/60/90 ngày tùy data window
- tracking/shop/creative reads nếu available

### Deliverable

- inventory account
- active/disabled/deleted visibility caveat
- spend and performance summary
- tracking readiness
- naming/structure quality
- urgent risks
- 7-day action plan

### Giá trị vận hành

Giúp tránh nhận account mù, đặc biệt khi khách chỉ add user vào Business Center mà không có tài liệu bàn giao.

## Case 13: Experiment design từ historical winners

### Bối cảnh

Account có một số campaign/ad cũ từng chạy. Muốn thiết kế test mới dựa trên dữ liệu cũ.

### MCP reads

- historical campaign/ad reports
- ad metadata
- daily trend

### Phân tích

- ad/campaign nào thắng theo metric phù hợp objective
- signal nào chưa đáng tin vì spend thấp/sample nhỏ
- angle nào cần lặp lại
- biến thể nào nên test có kiểm soát

### Output

- hypothesis
- control creative/campaign
- variants
- budget split draft
- stop/continue criteria
- measurement window

## Case 14: Policy and approval status review

### Bối cảnh

Ads không chạy hoặc phân phối yếu, nghi do approval/policy/status.

### MCP reads

- `campaign_get`
- `adgroup_get`
- `ad_get`
- status/review/rejection fields nếu tool schema trả được

### Output

- object nào bị disable/reject/limited
- campaign/adgroup/ad nào là nguyên nhân downstream
- rejection reason nếu API trả
- đề xuất sửa copy/landing/creative ở dạng draft

### Guardrail

Không hướng dẫn né policy. Chỉ đề xuất sửa để rõ ràng, đúng claim, đúng landing, đúng ngành hàng.

## Case 15: Internal sales demo

### Bối cảnh

Diginno muốn demo năng lực “AI Ads Ops” cho khách tiềm năng.

### Flow demo

1. OAuth vào account demo/được phép.
2. MCP read account/campaign/report.
3. Sinh report insight trong 2-5 phút.
4. Sinh audit sơ bộ với caveat rõ.
5. Sinh action plan không write.

### Demo boundary

- không dùng account khách thật nếu chưa có duyệt
- không show token/secret
- không show dữ liệu nhạy cảm ra public
- nói rõ demo-ready khác với full audit

## Mapping case study với skill

| Case | Skill chính | Tool nhóm chính |
| --- | --- | --- |
| Account smoke test | `tiktok-ads-official` | user/auth/advertiser |
| Campaign report | `tiktok-ads-report-insight` | campaign/report |
| Creative signal | `tiktok-ads-creative-review` | ad/report |
| Zero conversion | `tiktok-ads-audit` | campaign/adgroup/report/pixel |
| Budget pacing | `tiktok-ads-report-insight` | daily report/campaign |
| Objective mismatch | `tiktok-ads-audit` | campaign/report |
| Pre-launch QA | `tiktok-ads-launch-plan` | read current state, draft write |
| Shop/GMV Max | `tiktok-ads-official` + audit | shop/gmv max |
| Creative brief | `tiktok-ads-creative-review` | ad/report/creative |
| Monthly report | `tiktok-ads-report-insight` | report hierarchy |
| Anomaly monitor | `tiktok-ads-report-insight` | status/report |
| Handover audit | `tiktok-ads-audit` | full hierarchy/report |
| Experiment design | `tiktok-ads-audit` + creative | historical report/ad |
| Policy review | `tiktok-ads-audit` | object status/rejection |
| Sales demo | all read-only skills | account/report/audit |

## Next repo ideas

- Add sample prompts per case.
- Add report templates for client-facing Markdown.
- Add JSON schema for audit bundle.
- Add command snippets for common MCP reads.
- Add sanitized sample output from a demo account.
