# Giai đoạn 06 — ứng dụng mobile

## Bắt đầu từ bộ bàn giao cho Hy

[T-024 — Bộ bàn giao app cho Minh Hy](T-024-ban-giao-app-cho-hy/T-024-README.md) gom context, role/quyền, workflow/policy/cases, S4/S8 contract, model/hash/code/runtime và checklist integration. Policy đã chốt; app/adapter còn cần implement. [DECISION_LOGIC](DECISION_LOGIC.md) ghi vì sao chuyển từ nghiên cứu sang integration.

**Thứ tự hiện tại:** build app → nối business/observation/S4/S8/retry/manual/write → chạy được end-to-end → freeze input/config/case cho test cuối → test/report. Test-profile preparation là checklist về sau, không cản bắt đầu app.

Khi Hy chọn nền tảng/nơi chạy AI, ghi tài liệu `<TASK-ID>-design.md`: camera/input, reference mapping, AI contract, logic check-in tách attendance/entry, lưu/hiển thị, quyền và model assets. Không mặc định on-device hay server trước quyết định. Hai bề mặt thí sinh/người phụ trách không bắt buộc là hai app hoặc hai thiết bị riêng.

**Kiểm khi tích hợp:** khai SBD → business pre-check → observation → S4/S8 → final-check → confirmed write hoặc retry/manual/hold → xem kết quả/audit. Khi có mã, bổ sung build/run, thiết bị, config/version và giới hạn; model research threshold chưa tự là cấu hình demo đã freeze.
