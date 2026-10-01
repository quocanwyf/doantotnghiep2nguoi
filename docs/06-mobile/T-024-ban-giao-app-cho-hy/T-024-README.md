# T-024 — Bộ bàn giao ngữ cảnh làm app cho Minh Hy

**Cập nhật:** 2026-10-01. **Người chuẩn bị:** Quốc An, Codex hỗ trợ. **Mục đích:** Hy có thể bắt đầu xây app/integration từ nghiệp vụ đã chốt và pipeline AI đang có, không phải đọc lại toàn bộ lịch sử thí nghiệm.

## Đọc theo thứ tự

| File | Hy sẽ biết gì? |
| --- | --- |
| [01 — Context và phạm vi](T-024-01-context-va-pham-vi.md) | Bài toán, hai bề mặt sử dụng, trách nhiệm An/Hy và thứ tự build app. |
| [02 — Role và quy trình](T-024-02-role-va-quy-trinh.md) | Loại người dùng, quyền, main flow và nghĩa outcome. |
| [03 — Policy và case](T-024-03-policy-va-case.md) | Default đã duyệt, ngoại lệ, retry và những giá trị Hy cần cấu hình. |
| [04 — S4/S8 và contract AI](T-024-04-s4-s8-va-ai-contract.md) | AI nhận/trả gì, selection khác verification, cách nối một mặt/nhiều mặt. |
| [05 — Model, code và runtime](T-024-05-model-code-va-runtime.md) | Đúng file ONNX, hash, code có thể tái dùng, cách khởi tạo runtime tham chiếu. |
| [06 — Assets và checklist integration](T-024-06-assets-va-checklist-integration.md) | File trong/ngoài Git, dữ liệu demo, phần cần implement và kiểm khi app chạy được. |

## Trạng thái bàn giao

- **Đã chốt:** bốn group policy demo D-004–D-007; default/retry, quyền auto-check-in có điều kiện, manual authority và cách báo test.
- **Đang có:** detector/encoder và code nghiên cứu S4/S8; kết quả T-023 hỗ trợ giữ MobileFaceNet làm mốc để tích hợp. Chưa có checkpoint mới do train/fine-tune.
- **Cần xây:** UI, quản lý attempt, business checks, adapter AI, retry/manual, confirmed write và audit. Bộ tài liệu này không phải app/SDK đã chạy.
- **Bước thực hiện:** làm app → nối pipeline → chạy được end-to-end → freeze cấu hình/case/input cho test cuối → test/report. [Test-profile preparation](../../01-problem/T-024-test-profile-preparation.md) là checklist dùng về sau, không là điều kiện phải hoàn thành trước khi build.

## Nguồn chính thức và cách dùng bộ này

Đây là bản hướng dẫn đọc/triển khai, không tạo policy thứ hai. Khi cần chi tiết hoặc phát hiện khác nhau, đối chiếu [workflow](../../01-problem/T-024-demo-decision-policy.md), [AI/retry](../../01-problem/T-024-ai-rule-and-retry.md), [business policy](../../01-problem/T-024-business-policy.md) và các quyết định:

- [D-004 — Default demo](../../00-project/decisions/T-024-D-004-duyet-default-demo.md).
- [D-005 — Auto-check-in](../../00-project/decisions/T-024-D-005-auto-checkin-co-dieu-kien.md).
- [D-006 — Manual authority](../../00-project/decisions/T-024-D-006-manual-authority.md).
- [D-007 — Workflow và risk evaluation](../../00-project/decisions/T-024-D-007-workflow-va-risk-evaluation.md).
- [D-008 — Bàn giao và build app trước test cuối](../../00-project/decisions/T-024-D-008-ban-giao-va-build-app.md).

Tên field/DTO hoặc nhánh adapter ghi **Đề xuất integration** chưa phải API hay quyết định kỹ thuật đã triển khai. Hy được chọn UI, mobile stack, cách tổ chức module/service và chi tiết app; ghi quyết định cùng lý do. Thay đổi capability cốt lõi hoặc rule AI cần trao đổi với An và version rõ.

**GitHub:** bộ này nằm trong [PR #19](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/19), branch `codex/T-024-demo-policy`, xếp sau PR #18. Khi PR chưa merge, chỉ pull `main` có thể chưa thấy tài liệu này; đọc Files changed hoặc dùng branch PR trong checkout phù hợp. Trạng thái task theo [Sheet chung](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0).

**Giới hạn chung:** `θ=0.23` là research/reference operating point, chưa là demo threshold đã freeze/kiểm đạt. False-accept cap còn TBD. Proxy/replay và fixture không chứng minh hiệu quả camera cửa phòng thi thật; policy không tự loại bỏ các hard-negative acceptance đã quan sát.
