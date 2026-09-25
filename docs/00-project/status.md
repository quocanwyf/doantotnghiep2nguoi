# Trạng thái dự án

- Cập nhật: 2026-09-25
- Giai đoạn: đề xuất bài toán (01) và khảo sát kỹ thuật (02) đã có đầu ra trên PR, đang chờ review/thống nhất.
- Thành viên: Quốc An (TV-A), Minh Hy (TV-B).

## Đã có đầu ra

- [PR #1 — T-002/T-005](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/1) đang ở trạng thái draft: đề xuất của Quốc An về thiết bị tại cửa phòng thi, luồng khai báo mã rồi xác minh khuôn mặt 1:1; bộ khảo sát theo stage, dữ liệu, model family/candidate và kế hoạch thí nghiệm. [Logic 01](../01-problem/DECISION_LOGIC.md) và [logic 02](../02-survey/DECISION_LOGIC.md) nối rõ vì sao mỗi bước phát sinh. Cập nhật rationale đã được push tại commit f8586a5.
- [PR #2 — T-003/T-006](https://github.com/quocanwyf/doantotnghiep2nguoi/pull/2) đang mở: đề xuất bài toán và khảo sát độc lập của Minh Hy để hai người review, so sánh.
- Các tài liệu trên là đề xuất/survey và thiết kế phép thử. Chưa có kết quả benchmark, pilot hoặc phép đo giảm nhân sự thực tế.

## Chưa chốt và giới hạn

- **T-004:** Quốc An thông báo nhóm đã chọn hướng cửa phòng thi; PR #2 ghi T-004 chưa chốt. Sheet chưa có trạng thái hoàn tất và [thư mục quyết định](decisions/) chưa có biên bản ngày, người chốt, nguồn. Cần hai thành viên xác nhận rồi mới ghi phương án chính thức.
- **T-007:** chưa có biên bản so sánh hai khảo sát và lựa chọn candidate chung để đưa vào experiment. Shortlist T-005 không phải final technical decision.
- Chưa xác minh đầy đủ tệp/quyền dùng dataset và trọng số, chưa khóa protocol/split/metric/operating point, chưa chọn thiết bị và giới hạn latency/RAM, chưa chạy baseline hoặc phân tích lỗi. Dataset/model/threshold/optimization và mobile stack cuối vẫn mở.
- Dữ liệu công khai có thể đánh giá thành phần thị giác theo protocol phù hợp; hồ sơ giả lập chỉ kiểm thử logic nghiệp vụ. Hai nguồn này không chứng minh hiệu quả vận hành tại kỳ thi thực tế.

## Bước tiếp theo theo thứ tự

1. **T-004 — chốt nghiệp vụ:** Quốc An và Minh Hy review chéo T-002/T-003, xác nhận hướng cửa phòng thi và phạm vi kỳ thi mục tiêu. Ghi scope.md, biên bản/quyết định có ngày, người chốt và nguồn; tách điều nhóm thống nhất khỏi điều cần thầy hoặc đơn vị tổ chức xác nhận. Làm rõ actor, quy trình hiện tại, quyền xử lý ngoại lệ, muộn/nhầm phòng/chưa đến, giấy tờ và mức tự động hóa được phép.
2. **T-007 — chốt phương án đem thử:** đối chiếu T-005/T-006 theo cùng use case và requirement; nêu vì sao dataset/model family/candidate đáp ứng yêu cầu, gap dữ liệu, rủi ro và câu hỏi experiment cần phân xử. Chỉ chọn candidate và protocol dự kiến, chưa gọi đó là lựa chọn kỹ thuật cuối.
3. **Trước baseline:** kiểm tra quyền/tệp/weight/preprocessing, thiết lập manifest và split tránh rò rỉ, chốt metric và acceptance criteria có nguồn, chọn thiết bị đo. Sau đó chạy baseline cùng điều kiện, phân tích lỗi để xác định bottleneck trước khi chọn hướng tối ưu.

**Task, người phụ trách và trạng thái chi tiết:** [Google Sheet chung](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0). Trang này tóm tắt tiến độ và việc kế tiếp, không sao chép bảng task.
