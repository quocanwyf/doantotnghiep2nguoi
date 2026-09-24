# Kịch bản T-004 nếu nhóm chọn đề xuất của Quốc An

**Trạng thái:** bản giả định để trao đổi, do Quốc An đề xuất. Chưa có bản T-003 của Minh Hy để so sánh, nên tài liệu này **không phải scope.md hoặc quyết định chính thức của nhóm**. Không cập nhật trạng thái T-004 trên Sheet từ tài liệu này.

## Gói phương án Quốc An muốn đưa ra so sánh

- **Bối cảnh:** làm thủ tục tại cửa phòng thi, có danh sách và ảnh đăng ký theo kỳ thi, phòng, ca từ trước.
- **Vấn đề:** giám thị cần xác định đúng người, đúng phòng/ca, tránh lượt trùng, xử lý dòng thí sinh đông và có nhật ký đối soát.
- **Người và camera:** một thí sinh đứng trong vùng kiểm tra mỗi lượt; điện thoại cố định ở cửa, có thể nhìn thấy người khác trong nền. Giám thị xem kết quả và quyết định các ngoại lệ theo quy chế.
- **Luồng chính:** thí sinh khai báo mã → lấy đúng hồ sơ → chọn mặt người đang làm thủ tục → xác minh 1:1 với ảnh đăng ký → kiểm tra phòng, ca, giờ và trạng thái → hiển thị chấp nhận sơ bộ/chụp lại/chuyển giám thị → ghi sự kiện.
- **Phạm vi đầu ra:** hỗ trợ kiểm tra danh tính và ghi nhận lượt vào. Chưa tuyên bố tự động mở cửa, thay giám thị, xác thực CCCD thật hay chống mọi hình thức giả mạo.
- **Dữ liệu dự kiến:** ảnh đăng ký và lượt qua camera cửa phòng được thu có quyền sử dụng, gồm đúng người, người khai báo mã sai, người ngoài danh sách và điều kiện đông/sáng khác nhau. Nguồn công khai chỉ hỗ trợ phép thử thành phần, không thay thế dữ liệu tại cửa.
- **Baseline kỹ thuật:** phát hiện/căn chỉnh mặt, embedding cố định, một ảnh/lượt và ngưỡng 1:1 hiệu chỉnh trên tập phát triển. Model cụ thể và giấy phép phải được kiểm chứng.
- **Hướng cải thiện ứng viên:** tập trung kiểm tra lỗi chọn mặt/khung hình trong ảnh nguyên khung; nếu lỗi có thật, so quy tắc một khung với chọn nhiều khung theo chất lượng và theo dõi người trong vùng. Ngưỡng và chính sách chụp lại có thể khảo sát riêng. Chưa khẳng định đây là đóng góp cuối cùng trước khi có baseline và dữ liệu.
- **Đo lường:** FMR/FNMR của xác minh, lỗi chọn nhầm mặt, lỗi quyết định ở cấp lượt vào, tỷ lệ chuyển thủ công, chụp lại và thời gian/lượt; độ trễ/bộ nhớ trên cùng điện thoại. Đặt giới hạn nhận nhầm theo nghiệp vụ rồi xem đánh đổi với bỏ sót và thời gian. Không so số liệu giữa các dataset khác nhau như cùng một phép thử.
- **Rủi ro:** ảnh đăng ký không đáng tin, thiếu quyền dùng dữ liệu thật, ảnh/video giả mạo, khẩu trang, quy chế yêu cầu kiểm tra giấy tờ, quá ít mẫu để ước lượng lỗi hiếm, thiết bị không đại diện điều kiện cửa phòng.

## Vì sao Quốc An đề xuất phương án này

Bài toán có quyết định nghiệp vụ rõ ở mỗi lượt, danh sách phòng/ca đã biết và camera mobile có vai trò trực tiếp. Luồng khai báo mã rồi xác minh 1:1 thu hẹp đối tượng so sánh, giúp đặt metric và xử lý sai sót rõ hơn tìm toàn bộ danh sách 1:N. Môi trường cửa phòng vẫn tạo ca khó đáng nghiên cứu: nhiều người trong nền, ánh sáng/góc mặt thay đổi và áp lực thời gian. Mục tiêu sản phẩm lâu dài là một thiết bị hỗ trợ nhiều phòng; mục tiêu đồ án là chứng minh một cải thiện kỹ thuật trong phạm vi được đo.

## Phần T-004 thật phải làm sau khi có T-003

1. Đọc trọn đề xuất bài toán **và kỹ thuật** của Minh Hy, không chỉ so tên bối cảnh.
2. So sánh hai gói phương án theo: mức rõ của nghiệp vụ; dữ liệu và quyền dùng; baseline; điểm lỗi có thể tối ưu; giao thức đo; khả năng demo mobile; chi phí và rủi ro.
3. Hai người chọn hoặc chỉnh một phương án chính, ghi lý do chọn/loại và phần nào còn chờ thầy xác nhận.
4. Khi cả hai thống nhất mới viết docs/01-problem/scope.md và file quyết định có ngày, người chốt và nguồn theo quy trình repo.
5. Trước thí nghiệm sâu, có một checkpoint đặc tả nghiệp vụ cho phương án được chọn: mỗi ngoại lệ có điều kiện phát hiện, hành động, người quyết định, bằng chứng và cách sửa sai.

## Điều chỉnh trình tự task cần nhóm xác nhận

Cách phân việc Quốc An vừa nêu là: **T-002 và T-003 mỗi người chuẩn bị một phương án đầy đủ từ nghiệp vụ đến khảo sát kỹ thuật sơ bộ; T-004 so sánh các phương án đầy đủ rồi chọn**. Cách này khác mô tả cũ rằng chọn bối cảnh ở T-004 xong cả hai lại khảo sát kỹ thuật độc lập ở T-005/T-006. Sau khi thống nhất với Minh Hy, nhóm cần cập nhật Sheet và README giai đoạn 01–02 để T-005/T-006/T-007 có vai trò mới rõ ràng, chẳng hạn kiểm chứng dữ liệu/baseline và chốt thiết kế thí nghiệm của phương án đã chọn. Bản giả định này chưa tự đổi task của Minh Hy hoặc đánh dấu task nào hoàn thành.
