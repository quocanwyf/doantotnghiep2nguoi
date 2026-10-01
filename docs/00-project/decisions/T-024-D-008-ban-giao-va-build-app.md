# T-024 / D-008 — Bàn giao ngữ cảnh và chuyển sang build app

- **Ngày:** 2026-10-01.
- **Người chốt:** Quốc An.
- **Nguồn:** Quốc An xác nhận trong chat: sau T-024 chuyển app/integration; test-profile là checklist cuối sau khi app chạy, và yêu cầu tạo folder MD bàn giao cho Hy gồm policy/business/role/S4/S8/model/code.

## Quyết định và lý do

T-024 D-004–D-007 đã đủ contract demo; T-023 chưa có evidence buộc thay/fine-tune encoder. Tiếp theo implement app/integration từ [bộ bàn giao Hy](../../06-mobile/T-024-ban-giao-app-cho-hy/T-024-README.md), không mở thêm nhánh nghiên cứu model/threshold hoặc phase chuẩn bị test lớn.

**Thứ tự:** UI/business → observation/adapter S4/S8 → retry/manual/final-check/write/audit → end-to-end hoạt động → freeze config/input/case trước test cuối → test/report. Hy chọn UI/stack/chi tiết nghiệp vụ app và ghi quyết định; An bàn giao/hỗ trợ AI research configuration/evidence.

## Ranh giới và việc kế tiếp

Đây là quyết định thứ tự công việc/bàn giao, không duyệt SDK/dispatcher/architecture hoặc demo threshold mới. P2 nghiên cứu chỉ nhận ≥2 scores; nhánh dispatcher một mặt trong bộ bàn giao là đề xuất integration cần implement/version/kiểm. θ=0.23 vẫn research reference. Model pack chưa xác nhận Hy đã nhận; không đưa weight/ảnh/identity vào Git. Cap TBD và giới hạn proxy của D-007 giữ nguyên.

App chạy được rồi mới cụ thể hóa checklist test-profile; freeze vẫn phải trước test chính thức. Không sửa/tune holdout cũ để làm đẹp kết quả integration.
