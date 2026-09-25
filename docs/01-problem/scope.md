# Phạm vi bài toán nhóm đã chọn — T-004

**Quyết định:** [D-001](../00-project/decisions/D-001-chon-bai-toan-cua-phong-thi.md). Quốc An xác nhận ngày 2026-09-25 rằng Quốc An và Minh Hy đã chốt đề tài từ T-002. [Logic dẫn tới lựa chọn](DECISION_LOGIC.md) ghi chuỗi suy luận; hai đề xuất cá nhân vẫn được giữ nguyên để đối chiếu.

## Bài toán nghiệp vụ

Tại cửa phòng thi, thiết bị hỗ trợ kiểm tra đầu vào thường lệ: thí sinh khai báo mã; hệ thống lấy hồ sơ và ảnh đăng ký, kiểm tra người trước camera có khớp hồ sơ, đúng phòng/ca/giờ và chưa ghi lượt trùng; trả kết quả rõ lý do để ghi nhận hoặc chuyển người phụ trách. Mục tiêu là giảm công đối chiếu lặp lại tại từng phòng và hỗ trợ đối soát người hợp lệ, đến muộn, nhầm phòng, chưa đến cùng ngoại lệ. Mức giảm nhân sự là mục tiêu cần pilot đo, không phải kết quả đã chứng minh.

**Actor:** thí sinh; giám thị/người phụ trách phòng xử lý ngoại lệ; đơn vị tổ chức quản lý danh sách, phòng/ca, quyền và quy tắc. Quy trình hiện tại và quyền quyết định cuối cần xác nhận cho kỳ thi cụ thể. Không mặc định bỏ bước kiểm tra trực tiếp mà quy chế yêu cầu.

## Vì sao T-002 thay vì T-003

[T-002](quoc-an-proposal.md) gắn mỗi lượt với một phòng/ca đã định và mã hồ sơ, nên phát sinh xác minh 1:1 cùng quy tắc nghiệp vụ. [T-003](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/2) ưu tiên điểm danh lớp 1:N theo phiên học; actor, trạng thái và hậu quả lỗi khác. Nhóm chọn đề tài phù hợp mục tiêu cửa phòng thi trước, rồi mới chọn hướng khảo sát kỹ thuật tương ứng ở T-007.

## Ranh giới và câu hỏi mở

- **Trong phạm vi nghiên cứu hiện tại:** phân rã pipeline, khảo sát dữ liệu/model theo stage, baseline và thí nghiệm có đối chứng; kiểm thử logic nghiệp vụ bằng hồ sơ giả lập. Dữ liệu thị giác dự kiến từ nguồn công khai có quyền dùng phù hợp.
- **Chưa được phép kết luận:** hệ thống thay giám thị, giảm được một số người cụ thể, hoạt động tin cậy với thí sinh thật/camera cửa phòng thực, hoặc chống ảnh/video giả khi chưa có module và phép thử tương ứng.
- **Cần đặc tả tiếp:** kỳ thi mục tiêu/quy chế; quy trình hiện tại; cách nhập mã; quyền xử lý muộn, nhầm phòng, trùng lượt, chưa đến và sửa sai; dữ liệu ảnh tham chiếu; thiết bị/kết nối; giới hạn thời gian và tỷ lệ sai chấp nhận/từ chối.

**Đầu ra cho phase 02:** một lượt có mã khai báo và ảnh kiểm tra dẫn tới verification 1:1; rule phòng/ca/giờ và audit là các stage riêng. [D-002](../00-project/decisions/D-002-chon-huong-khao-sat-t005.md) ghi hướng khảo sát nhóm chọn để thử các phần chưa chắc.
