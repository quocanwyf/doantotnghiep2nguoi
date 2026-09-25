# D-001 — Chọn bài toán kiểm tra thí sinh tại cửa phòng thi

- **Trạng thái:** Nhóm đã chốt; chưa ghi nhận xác nhận của thầy.
- **Ngày ghi nhận:** 2026-09-25. Ngày hai thành viên thảo luận/chốt trước đó chưa được cung cấp.
- **Người chốt:** Quốc An và Minh Hy, theo xác nhận trực tiếp của Quốc An trong trao đổi ngày 2026-09-25.
- **Nguồn:** Xác nhận trên; [đề xuất T-002 của Quốc An](../../01-problem/quoc-an-proposal.md) và [đề xuất T-003 của Minh Hy](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/2). Đây là quyết định của nhóm, không suy ra thầy đã duyệt quy trình kỹ thuật hay mức thay thế giám thị.

## Vấn đề và phương án

Mục tiêu nghiệp vụ là để thiết bị tại cửa đảm nhận bước kiểm tra đầu vào thường lệ, giảm nhu cầu một người chỉ đứng đối chiếu ở mỗi phòng, đồng thời ghi nhận người hợp lệ, đến muộn, nhầm phòng, chưa đến và ngoại lệ để đối soát. T-002 đề xuất cửa phòng thi với danh sách phòng/ca có trước và mã thí sinh khai báo trước khi xác minh mặt 1:1. T-003 đề xuất điểm danh lớp bằng điện thoại, ưu tiên nhận dạng 1:N trong danh sách phiên học.

## Lựa chọn và lý do

Nhóm chọn **bài toán T-002 tại cửa phòng thi**. Phương án này giải quyết đúng sự kiện nghiệp vụ cần hỗ trợ: một lượt thí sinh vào **một phòng/ca**, có danh sách và mã hồ sơ để đối chiếu, rồi cần trả trạng thái và ghi vết. Luồng T-003 phục vụ điểm danh lớp và đặt câu hỏi nhận dạng 1:N khác; không dùng nó làm bài toán chính chỉ vì có candidate model/dataset sẵn.

Trong T-002, mã chọn hồ sơ chứ không chứng minh danh tính; bước thị giác cần kiểm tra người đứng trước camera với ảnh hồ sơ (**verification 1:1**). Phòng/ca/giờ/trùng lượt là rule/database, không phải nhãn mà model khuôn mặt suy ra. Thiết bị xử lý lượt thường lệ và chuyển trường hợp không chắc cho người có thẩm quyền; mức tự động hóa thực tế phụ thuộc quy chế kỳ thi mục tiêu.

## Bằng chứng, giới hạn và ảnh hưởng

Bằng chứng cho lựa chọn phạm vi là yêu cầu nghiệp vụ và hai đề xuất, **không phải** benchmark/pilot. Chưa có số đo giảm nhân sự, chưa chọn loại kỳ thi/quy chế cụ thể, dataset, model, threshold hay mobile stack. [Scope phase 01](../../01-problem/scope.md) ghi ranh giới; [logic 01](../../01-problem/DECISION_LOGIC.md) nối sang yêu cầu kỹ thuật. Quyết định này là đầu vào bắt buộc cho T-007 và khảo sát 1:1 ở T-005. Khi có ý kiến thầy/đơn vị tổ chức, ghi biên bản trước rồi cập nhật phạm vi và quyết định nếu cần.
