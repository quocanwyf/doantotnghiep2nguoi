# D-004 — Duyệt Group 1: default config cho demo T-024

- **Trạng thái:** Approved for demo profile — chỉ Group 1, chưa freeze toàn bộ T-024.
- **Ngày/người chốt:** 2026-09-30, Quốc An.
- **Nguồn:** xác nhận trực tiếp trong cuộc trò chuyện: “mình duyệt nhóm 1”, kèm hai chỉnh wording về global capture cap và AIConfig. Không tự ghi nhận phê duyệt thêm của Minh Hy/thầy hoặc quy chế kỳ thi thật.
- **Vấn đề:** demo cần default vận hành rõ để triển khai workflow; giới hạn theo từng lý do không được cộng thành retry vô hạn, và default nghiệp vụ không được hiểu là quyết định threshold triển khai.

## Lựa chọn được duyệt

- Muộn trong giới hạn 15 phút, intake còn mở → LATE + CONTINUE các kiểm khác; quá 15 phút → MANUAL. Ca đóng xử lý theo lifecycle riêng. Early check-in window vẫn **TBD**.
- Technical recovery = 1; no-face/poor-quality/S4 unresolved có tối đa 2 retry mỗi nhóm; S8 not verified = 1 capture mới. **Mọi retry capture đều chịu `max_capture_attempts = 3` cho toàn attempt**, gồm initial capture. Không cộng dồn ngân sách các nhóm. Bảng key/counter duy nhất ở [AI/retry, mục 5](../../01-problem/T-024-ai-rule-and-retry.md#5-retrypolicy--một-nguồn-và-ngân-sách-toàn-attempt).
- Re-entry/already checked-in → MANUAL, không tạo duplicate effective check-in.
- ELIGIBLE → CONTINUE; CANCELLED/SUSPENDED/DISQUALIFIED → CHECK_IN_NOT_ALLOWED; PENDING/UNDER_REVIEW/UNKNOWN/conflict → MANUAL. Status lấy từ dữ liệu có thẩm quyền.
- Missing/unusable reference → MANUAL; policy/roster unreliable → SYSTEM_HOLD.

**Wording đã duyệt:** T-024 không thay model, P2 hoặc retune S8. AIConfig hiện tại được giữ nguyên làm cấu hình nghiên cứu tham chiếu; operating point dùng cho end-to-end demo sẽ được freeze trước khi test và không được tuning từ chính test đó. `θ=0,23` T-023 chưa là threshold demo/deployment đã được chứng minh.

## Lý do, tác động và giới hạn

Default giúp app có hành động cụ thể, còn global cap giới hạn toàn lượt thay vì cộng no-face + quality + S4 retries. Technical recovery cùng input có budget riêng, không là evidence danh tính mới. Chưa có kết quả chạy để kết luận các default này giảm false acceptance hoặc đạt yêu cầu hiệu năng.

Group 2 (quyền auto-check-in), Group 3 (manual authority), Group 4 (risk/test acceptance) còn cần chốt. Quality/temporal capability, manual timeout và các retry phụ ngoài nhóm đã xác nhận vẫn theo trạng thái ở tài liệu. Không bật quyền auto-PASS từ việc duyệt Group 1; không sửa model/protocol/kết quả cũ.

**Bước tiếp:** chốt Group 2: business OK + AI_VERIFIED được tự ghi check-in hay cần người xác nhận cuối; sau đó manual authority và risk trước freeze/test. Quyết định này duyệt các default của draft, không thay D-001/D-002/D-003.
