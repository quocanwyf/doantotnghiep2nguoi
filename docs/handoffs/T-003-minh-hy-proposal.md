# Bàn giao T-003 — đề xuất use case của Minh Hy

- **Người làm, ngày:** Minh Hy, 2026-09-24.
- **Link task trên Sheet:** [T-003, Trang tính1](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0).
- **Commit/PR:** Báo cáo ban đầu ở commit `8a1a679`, phần bổ sung optimization ở `ee6de56`, trên nhánh `task/T-003-minh-hy-proposal`. PR chưa tạo do GitHub từ chối push với mã 403 cho tài khoản `Minh-Hy`.
- **Tóm tắt và file chính:** [Bản đề xuất](../01-problem/minh-hy-proposal.md) so sánh check-in từng người với chụp nhiều người trong lớp; trình bày người dùng, camera, đầu ra, logic điểm danh, tiêu chí đo, giả định, MobileFaceNet, các nguồn dữ liệu và hai hướng optimization: tham số huấn luyện hoặc bounding box/ROI.
- **Cách kiểm tra và kết quả thực tế:** Đọc từng mục trong bản đề xuất; đối chiếu các liên kết nguồn gốc model/dataset và hai use case với yêu cầu trong `../01-problem/README.md`. Đây là phân tích tài liệu, **chưa có huấn luyện, thử nghiệm trên điện thoại hoặc số liệu hiệu năng của nhóm**.
- **Quyết định/giả định:** Use case A, MobileFaceNet, DigiFace-1M và cả hai hướng optimization đều là **đề xuất**. Chỉ chọn một điểm tối ưu chính sau thử nghiệm chẩn đoán và thảo luận nhóm. Không có quyết định kỹ thuật mới. Mọi số liệu benchmark trong báo cáo đều ghi là số liệu của nguồn tham khảo, không phải kết quả đồ án.
- **Điều chưa xong và người tiếp tục:** Quốc An review ở T-003; hai người so sánh với T-002 và chọn phạm vi ở T-004. Cần xác nhận quyền thu dữ liệu thật, ngân sách huấn luyện, thiết bị và yêu cầu của thầy trước T-006/T-007.
- **File ngoài Git:** Không có file mới cần bàn giao. Không đưa ảnh khuôn mặt hoặc embedding vào repo.
