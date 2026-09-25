# Giai đoạn 02 — khảo sát kỹ thuật

Hai thành viên khảo sát **độc lập toàn bộ bài toán đã chọn**: Quốc An làm T-005 cho bối cảnh xác thực thí sinh tại cửa phòng thi; Minh Hy làm T-006 theo phân công riêng. Ở T-007, hai người so sánh kết quả và ghi phương án nghiên cứu thống nhất trong [thư mục quyết định](../00-project/decisions/). Quốc An cho biết bối cảnh của mình đã được chọn ở T-004; biên bản quyết định và Sheet chưa được đồng bộ, nên đây là thông tin cần hoàn tất hồ sơ.

## Bộ tài liệu T-005 của Quốc An

Đọc theo thứ tự suy luận, không bắt đầu bằng tên dataset/model:

1. [Phân rã bài toán và phân loại task](quoc-an-task-decomposition.md): nghiệp vụ, xác minh 1:1, product/runtime pipeline, ML so với rule/database, giao diện và trường hợp lỗi.
2. [Yêu cầu và khảo sát dataset theo task](quoc-an-datasets.md): annotation, vai trò train/dev/test/external, candidate space, quyền và khoảng trống nhãn người mục tiêu.
3. [Yêu cầu và khảo sát phương pháp/model theo task](quoc-an-models.md): family → candidate → lọc → shortlist có điều kiện, phân biệt architecture/loss/weight/pipeline.
4. [Thiết kế benchmark và cổng quyết định tối ưu](quoc-an-experiments.md): metric từng task, baseline plan, phân tích lỗi/bottleneck, quyết định optimization sau baseline, ablation và điều kiện chọn pipeline cuối.

Các tài liệu trên **thay cho** bản khảo sát một file trước đây. Chúng là thiết kế nghiên cứu: chưa có final dataset/model/pipeline/optimization, chưa tải/kiểm tra trọn bộ dữ liệu, chưa chạy benchmark. Candidate shortlist giúp tạo phép thử; không phải kết quả đánh giá. PAD là task bổ trợ riêng; nghiệp vụ phòng/ca/giờ và ghi nhận là phần mềm có test riêng.

## Cổng chuyển sang thực nghiệm và T-007

Trước khi chạy, xác minh quyền dùng và phiên bản file/weight; chốt protocol, manifest cặp/lượt, tách dev/test theo identity hoặc phiên phù hợp, thiết bị đo, metric chính và operating point. Chạy baseline trước, phân tích lỗi có nhãn rồi mới chọn bottleneck và phương pháp tối ưu. Nếu làm nhiều can thiệp, có ablation đơn lẻ và kết hợp; so với chính baseline gốc lẫn pipeline mạnh khác. Chỉ chốt pipeline cuối khi có bằng chứng trên cùng dữ liệu/split/điều kiện đo.

Bộ khảo sát T-006 của Minh Hy giữ độc lập theo task của bạn ấy. T-007 ghi lý do chọn/loại và điều còn cần hỏi thầy; không tự coi shortlist T-005 là quyết định chung.
