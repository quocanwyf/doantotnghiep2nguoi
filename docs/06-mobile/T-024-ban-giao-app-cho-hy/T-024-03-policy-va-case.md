# T-024 — 03. Policy đã chốt và các case cần app support

Nguồn canonical: [business policy](../../01-problem/T-024-business-policy.md), [AI/retry](../../01-problem/T-024-ai-rule-and-retry.md), D-004–D-007. Default dưới là **profile demo được duyệt**, không phải quy chế kỳ thi thật.

## 1. Ba lớp riêng

- **Dữ liệu có thẩm quyền:** candidate/registration, room/session, eligibility, reference mapping, effective check-in. Không thay dữ liệu bằng config hoặc cosine.
- **ExamPolicy:** time, eligibility action, duplicate/re-entry, authority/manual routing, auto-check-in và RetryPolicy. Có owner/approver và version.
- **AIConfig:** detector/encoder/hash, preprocessing, S4 parameters, S8 rule/operating point và quality criterion nếu triển khai. Retry count không đặt thêm bản thứ hai ở đây.

## 2. Default và route

| Điều kiện | Xử lý đã chốt |
| --- | --- |
| Late ≤15 phút, intake còn mở | LATE + CONTINUE; vẫn kiểm identity và các điều kiện còn lại. |
| Late >15 phút, intake còn mở | MANUAL; room staff duyệt trong late delegation, không có quyền thì Admin. |
| Ca đóng | Nhánh lifecycle/Admin, không chỉ coi là late. |
| ELIGIBLE | CONTINUE. |
| CANCELLED/SUSPENDED/DISQUALIFIED | CHECK_IN_NOT_ALLOWED; room staff không tự bỏ blocked status. |
| Pending/unknown/conflict eligibility | MANUAL; giải quyết dữ liệu trước success. |
| Already checked-in / re-entry | MANUAL; giữ effective check-in cũ, không tạo record PASS thứ hai. |
| Reference thiếu/không dùng được | MANUAL; resolve source/mapping, không chữa bằng camera retry. |
| Policy/roster unreliable hoặc config lỗi | SYSTEM_HOLD; không auto-PASS. |
| Auto flag true + business/AI/final checks đạt | Confirmed write rồi PASS. |
| Auto flag false + lượt đạt | READY_FOR_CONFIRMATION → actor có quyền → recheck/write. |
| Write thất bại/không biết đã ghi chưa | SYSTEM_HOLD; reconcile trước lần ghi tiếp. |

Early check-in window còn **TBD**. Không tự hard-code 30 phút từ ví dụ. Arrival time giữ riêng với processing time; retry/chờ không tự sửa sự kiện đến. Hy cần định nghĩa nguồn clock và mốc late cho demo.

## 3. RetryPolicy: một nguồn, global cap

| Key | Default | Phạm vi |
| --- | ---: | --- |
| camera_technical_retry | 1 | Recovery chung lỗi mở camera/không lấy được frame. |
| no_face_retry | 2 | Capture bổ sung khi không detection. |
| poor_quality_retry | 2 | Capture bổ sung chung các lý do quality; tiêu chí phát hiện còn phải bind. |
| s4_unresolved_retry | 2 | Capture bổ sung khi không chọn được/candidate evidence mất hiệu lực. |
| s8_not_verified_retry | 1 | Capture mới sau NOT_VERIFIED. |
| processing_recovery_retry | 1 | Recovery cùng input hợp lệ; không là evidence mới. |
| max_capture_attempts | 3 | Initial + tối đa hai observation mới cho toàn attempt. |

Mọi capture mới phải còn **cả reason budget lẫn global budget**. Không cộng 2 no-face + 2 quality + 2 S4. Ví dụ capture1 no-face → capture2 quality fail → capture3 unresolved → MANUAL, không có capture4. Processing recovery trên capture3 có thể chạy nếu budget/input còn hợp lệ, nhưng không mở thêm capture.

Resume attempt, nhập lại cùng SBD hoặc reconnect không reset counters. Đổi claimed record phải kết thúc/ghi nhận lượt cũ và tạo lượt mới, không chuyển evidence A sang reference B. Optional instability/departure retry chưa được duyệt hoặc có tracking thực thi; không tự bật.

## 4. Nhóm case để triển khai

| Nhóm | Case app cần support | Đường xử lý |
| --- | --- | --- |
| Lookup | Không có hồ sơ; nhiều hồ sơ trùng mã; reference mapping mâu thuẫn | MANUAL/Admin; không chọn record theo score. |
| Context | Sai phòng/ca; chưa tới window; ca đóng | REDIRECT/WAIT hoặc authority theo policy; không chạy AI để sửa assignment. |
| AI input | No-face; ảnh không dùng được; camera/runtime lỗi | Retry/recovery đúng budget rồi MANUAL/SYSTEM_HOLD theo loại lỗi. |
| S4/S8 | Multi-face chọn được; unresolved; not verified | Chọn được → S8; chưa đủ → RETRY/MANUAL, không ép top-1/PASS. |
| Consistency | Duplicate, hai request gần nhau, resume, write timeout, roster/policy đổi giữa lượt | Final recheck, một effective record, giữ counter/version; unknown write → reconcile. |
| Human | READY confirm, manual identity, late exception, re-entry | Permission + scope + approved evidence; HUMAN giữ AI verdict gốc. |
| Recovery | Device/network/data fail, fallback, interrupted, unresolved cuối ca | Giữ case/audit; biên nhận tạm theo quyền; reconcile sau phục hồi. |
| Correction | Check-in/absence sai phát hiện sau | Admin, before/after/reason/evidence; attendance tách check-in. |

Danh sách này để Hy biết capability cần có, không bắt triển khai hết cùng một lúc. Khi nhánh chưa implement, báo trạng thái rõ và giữ pending/hold; không silently convert thành success.

## 5. Chi tiết app Hy cần quyết định

Account/delegation, evidence method manual, nguồn roster/reference và cập nhật, clock/window, timeout/retention, quality rule thực sự có, nơi chạy AI, giao diện/audit/storage. Ghi các lựa chọn trong task app của Hy với lý do và version; không biến TBD thành giá trị đã được nhóm chốt. Risk cap TBD không chặn build/demo, chỉ giới hạn kết luận safety.
