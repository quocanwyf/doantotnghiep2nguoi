# T-002 — Đề xuất use case của Quốc An

**Trạng thái:** Đề xuất cá nhân để trao đổi với Minh Hy. Chưa phải phạm vi chính thức của nhóm. Quốc An đề nghị khảo sát nhiều bối cảnh trước khi thu hẹp; Minh Hy chuẩn bị phương án riêng ở T-003.

## 1. Logic từ vấn đề đến đóng góp nghiên cứu

Với mỗi bối cảnh, trả lời theo thứ tự:

1. **Vấn đề nghiệp vụ:** việc ghi nhận hiện diện hoặc kiểm soát ra vào đang tốn công/sai ở đâu, hậu quả của từng loại sai là gì?
2. **Sự kiện cần quyết định:** ai được ghi có mặt, lúc nào, theo quy tắc nào, ai sửa trường hợp không chắc chắn?
3. **Bài toán thị giác:** chụp một hay nhiều người; xác minh danh tính đã khai báo (1:1), hay tìm người trong danh sách (1:N); có người ngoài danh sách không?
4. **Điều kiện camera:** vị trí, khoảng cách, ánh sáng, góc mặt, chuyển động, số người cùng lúc và thời gian xử lý.
5. **Giải pháp gốc:** thu ảnh → phát hiện/căn chỉnh mặt → tạo đặc trưng → so sánh → quyết định → ghi sự kiện và xử lý ngoại lệ.
6. **Đóng góp:** chỉ sau khi thử giải pháp gốc mới xác định điểm yếu, thay đổi có mục tiêu và so sánh bằng cùng dữ liệu, cách chia và điều kiện đo.

Phân biệt **cần** (thiếu thì không giải quyết được nghiệp vụ) với **muốn** (có thể là phần mở rộng). Nhận dạng đúng khuôn mặt không tự chứng minh người đó ở đúng địa điểm hoặc đang đứng trước camera thay vì ảnh/video; những yêu cầu này phải được nêu riêng.

## 2. Bảy use case ứng viên

### A. Điểm danh cả lớp bằng camera cố định

- **Vấn đề và người dùng:** giảng viên mất thời gian gọi tên; sinh viên vào muộn hoặc bị che khuất khiến danh sách dễ sai. Giảng viên xem và sửa kết quả.
- **Camera, input, bài toán:** camera trong phòng nhìn nhiều sinh viên từ xa. Nhận diện từng người trong danh sách lớp (1:N), đồng thời từ chối người ngoài danh sách.
- **Output và quy tắc hiện diện:** đề xuất danh sách có mặt theo buổi, kèm thời điểm quan sát; giảng viên xác nhận trước khi ghi chính thức. Phải định nghĩa cách xử lý vào muộn, ra sớm, bị che mặt.
- **Cần / muốn:** cần tránh tự ghi có mặt khi không quan sát đủ và có cơ chế sửa sai; muốn tự động xử lý toàn lớp.
- **Ràng buộc và dữ liệu:** mặt nhỏ, góc nghiêng, che khuất, ánh sáng không đều. Cần ảnh/video lớp học có nhiều buổi, nhãn người theo thời gian và quyền dùng phù hợp; ảnh chân dung đơn lẻ chưa đủ. Demo bằng selfie điện thoại không đại diện cho camera toàn lớp.
- **Giải pháp và điểm yếu có thể khảo sát:** phát hiện nhiều mặt → căn chỉnh → đặc trưng → so danh sách → gộp quan sát theo thời gian. Có thể thử chọn crop/khung hình hoặc quy tắc gộp; đo lỗi ghi có mặt/vắng mặt ở cấp buổi, tỷ lệ không xử lý được và tốc độ. Đây chỉ là hướng giả thuyết, chưa chọn thuật toán.

### B. Sinh viên tự điểm danh bằng điện thoại tại lớp

- **Vấn đề và người dùng:** giảng viên muốn giảm thao tác; sinh viên chủ động xác nhận, giảng viên xử lý ngoại lệ.
- **Camera, input, bài toán:** camera trước chụp một người sau khi sinh viên đăng nhập hoặc khai báo mã; xác minh 1:1 với mẫu đăng ký.
- **Output và quy tắc hiện diện:** chấp nhận, từ chối hoặc yêu cầu chụp lại; ghi theo buổi học. Cần quy định thế nào là “ở trong lớp”, chống dùng ảnh/video và xử lý mất mạng. Khuôn mặt một mình chưa giải quyết được các yêu cầu đó.
- **Cần / muốn:** cần xác minh người thực hiện và có đường sửa sai; muốn chạy hoàn toàn trên thiết bị, offline, chống giả mạo nâng cao.
- **Ràng buộc và dữ liệu:** ánh sáng/góc chụp/camera khác nhau; sai từ chối gây phiền, sai chấp nhận gây điểm danh hộ. Cần nhiều lần chụp mỗi người, cặp đúng/sai người, điều kiện thu ảnh gần thực tế và quyền đồng ý.
- **Giải pháp và điểm yếu có thể khảo sát:** phát hiện → kiểm tra chất lượng/căn chỉnh → đặc trưng → so 1:1 → ngưỡng. Có thể thử chọn mẫu đăng ký, kiểm tra chất lượng, căn chỉnh hoặc ngưỡng; đo tỷ lệ từ chối sai ở mức chấp nhận sai xác định trước, tỷ lệ phải chụp lại và độ trễ trên điện thoại.

### C. Nhân viên ghi nhận giờ vào/ra tại kiosk doanh nghiệp

- **Vấn đề và người dùng:** nhân sự cần sự kiện vào/ra đáng tin, ít nhập tay; nhân viên đứng trước camera ở điểm cố định.
- **Camera, input, bài toán:** camera kiosk chụp một người mỗi lượt. Nếu không nhập mã, tìm trong danh sách nhân viên (1:N và có “không biết”). Nhập mã rồi xác minh 1:1 là biến thể nghiệp vụ khác, phải đánh giá riêng.
- **Output và quy tắc hiện diện:** ghi thời điểm vào/ra và danh tính, hoặc chuyển lượt không chắc để duyệt. Ca làm, trùng lượt và sửa dữ liệu là quy tắc nghiệp vụ.
- **Cần / muốn:** cần hạn chế nhận nhầm và xử lý người chưa đăng ký; muốn không chạm, offline, chờ ngắn.
- **Ràng buộc và dữ liệu:** kính/khẩu trang, mẫu đăng ký cũ, danh sách tăng. Cần ảnh đăng ký và ảnh qua kiosk ở nhiều ngày, gồm cả người ngoài danh sách và quyền sử dụng ảnh nhân viên.
- **Giải pháp và điểm yếu có thể khảo sát:** pipeline một mặt → đặc trưng → tìm ứng viên → ngưỡng từ chối. Có thể thử chất lượng/cập nhật mẫu đăng ký, ngưỡng hoặc tìm kiếm gọn; đo nhận nhầm, bỏ sót người hợp lệ, thời gian mỗi lượt theo quy mô danh sách.

### D. Ghi nhận người dự họp trong phòng họp nhỏ

- **Vấn đề và người dùng:** chủ trì/thư ký mất thời gian điểm danh; cần biết ai thực sự dự một phiên.
- **Camera, input, bài toán:** camera cố định quan sát một nhóm nhỏ; nhận diện trong danh sách dự kiến (1:N), vẫn có khách ngoài danh sách.
- **Output và quy tắc hiện diện:** danh sách theo phiên và thời điểm được quan sát; chủ trì xác nhận. Cần định nghĩa xuất hiện bao lâu hoặc bao nhiêu lần thì tính có mặt.
- **Cần / muốn:** cần tránh ghi nhầm người chỉ xuất hiện thoáng qua; muốn tự động hỗ trợ người đến muộn và rời sớm.
- **Ràng buộc và dữ liệu:** quay mặt khỏi camera, che khuất, thay chỗ ngồi. Cần video có nhãn người/thời gian và quyền ghi hình; dataset ảnh tĩnh không kiểm tra được phần gộp theo thời gian.
- **Giải pháp và điểm yếu có thể khảo sát:** phát hiện nhiều mặt → đặc trưng từng khung → liên kết quan sát → quyết định ở cấp phiên. Có thể tối ưu chọn khung, gộp điểm hoặc ngưỡng; đo lỗi hiện diện theo phiên, tỷ lệ không rõ và tốc độ.

### E. Xác minh chủ thẻ tại cửa tòa nhà

- **Vấn đề và người dùng:** ban quản lý muốn giảm dùng thẻ mượn; người ra vào quét thẻ rồi nhìn camera.
- **Camera, input, bài toán:** camera ở cửa chụp một người, xác minh 1:1 với chủ thẻ. Bỏ thẻ và tìm toàn bộ danh sách là bài toán 1:N khác.
- **Output và quy tắc hiện diện:** đề xuất cho qua/từ chối/chuyển nhân viên trực. Cơ chế cửa và lối đi khẩn cấp phải được thiết kế riêng.
- **Cần / muốn:** cần rất hạn chế chấp nhận sai, có xử lý khi camera lỗi và quy trình dự phòng; muốn đi qua nhanh, ít tương tác.
- **Ràng buộc và dữ liệu:** ảnh/video giả mạo, ánh sáng ở cửa, người di chuyển nhanh, hậu quả của chấp nhận sai. Cần cặp đúng/sai người qua cửa, dữ liệu tấn công phù hợp, quyền dùng và khả năng thử nghiệm an toàn.
- **Giải pháp và điểm yếu có thể khảo sát:** kiểm tra chất lượng/chống giả mạo theo yêu cầu → xác minh → ngưỡng bảo thủ → ngoại lệ. Nếu thiếu dữ liệu giả mạo và hệ thống cửa, chỉ được kết luận về phần xác minh, chưa được tuyên bố giải quyết trọn bài toán.

### F. Ghi nhận khách đã đăng ký tại quầy lễ tân

- **Vấn đề và người dùng:** lễ tân muốn tìm đúng lịch hẹn nhanh hơn và hỗ trợ người không có đăng ký.
- **Camera, input, bài toán:** camera quầy chụp một người; so danh sách khách của ngày (1:N nhỏ, có người ngoài danh sách). Nếu khách đưa mã hẹn, chuyển thành xác minh 1:1.
- **Output và quy tắc hiện diện:** gợi ý lịch hẹn hoặc “không tìm thấy”; lễ tân xác nhận, không tự cấp quyền vào.
- **Cần / muốn:** cần tránh gán nhầm khách cho lịch hẹn khác; muốn giảm thời gian tìm và hạn chế lưu dữ liệu.
- **Ràng buộc và dữ liệu:** mẫu đăng ký có thể chỉ một ảnh, khách thay đổi diện mạo, danh sách thay hằng ngày. Cần ảnh đăng ký/ảnh tại quầy, người không có lịch, quy tắc lưu/xóa.
- **Giải pháp và điểm yếu có thể khảo sát:** tạo đặc trưng lúc đăng ký → so danh sách trong ngày → ngưỡng từ chối. Có thể thử chất lượng ảnh đăng ký, ngưỡng theo kích thước danh sách hoặc xử lý gọn trên mobile; đo gán sai lịch, bỏ sót khách và thời gian xử lý.

### G. Kiểm tra thí sinh tại cửa phòng thi theo phòng và ca

- **Vấn đề và người dùng:** đơn vị tổ chức thi có danh sách thí sinh, phòng và ca trước giờ thi; giám thị cần đối chiếu đúng người, đúng lịch, ghi nhận lượt vào và xử lý ngoại lệ giữa lúc nhiều người xếp hàng.
- **Camera, input, bài toán:** điện thoại đặt tại cửa. Một thí sinh bước vào vùng làm thủ tục mỗi lượt, dù có người khác ở hành lang hoặc trong nền ảnh. **Ưu tiên của Quốc An là thí sinh khai báo mã dự thi trước**, hệ thống lấy hồ sơ trong đúng kỳ thi/phòng/ca rồi xác minh mặt 1:1 với ảnh đăng ký. Chưa cần chọn ngay nhập số báo danh, quét mã trên giấy báo hay cách khác. Tìm mặt trực tiếp trong danh sách phòng (1:N) là phương án so sánh, chưa phải luồng chính được đề xuất.
- **Output và quy tắc:** xác minh được danh tính, đúng phòng/ca và chưa ghi nhận trùng thì đề xuất hoàn tất thủ tục; ảnh kém, mặt không khớp, sai phòng/ca, quá giờ hoặc hồ sơ bất thường chuyển đến giám thị/người có thẩm quyền. Một điểm số nhận dạng thấp không tự tước quyền dự thi. Quyết định cuối cùng và giấy tờ phải theo quy chế của từng kỳ thi.
- **Cần / muốn:** cần danh sách và ảnh đăng ký có nguồn tin cậy, kiểm tra đúng phòng/ca, chọn đúng người đang làm thủ tục, xử lý ngoại lệ và ghi vết; muốn giảm thao tác giấy tờ, kiểm tra nhanh và vận hành nhiều phòng bằng điện thoại hoặc thiết bị edge. Chống giả mạo phải được ghi là rủi ro ngay từ đầu; mức kiểm tra cần thiết phụ thuộc việc hệ thống chỉ hỗ trợ giám thị hay tự cho vào.
- **Ràng buộc và dữ liệu:** người đứng xung quanh, nhiều mức sáng, góc mặt, khẩu trang, lỗi chụp, người không có trong danh sách, lượt trùng, đến muộn và thay đổi phòng. Cần dữ liệu ảnh đăng ký và ảnh/video tại cửa được phép dùng, gồm người hợp lệ và các ngoại lệ; dữ liệu ảnh mặt đã cắt sẵn không kiểm tra được lỗi chọn nhầm người trong nền.
- **Giải pháp và điểm yếu có thể khảo sát sau T-004:** nhận mã khai báo → tìm hồ sơ → phát hiện đúng mặt trong vùng làm thủ tục → kiểm tra chất lượng/căn chỉnh → xác minh 1:1 → kiểm tra phòng, ca và trạng thái lượt vào → xử lý hoặc chuyển giám thị. Có thể khảo sát chọn mặt/khung hình, chất lượng ảnh, ngưỡng hoặc tốc độ trên mobile; đo nhận nhầm, bỏ sót, tỷ lệ chuyển thủ công, thời gian mỗi lượt và lỗi quyết định ở cấp lượt vào. Chưa chọn model hay thuật toán tối ưu.

## 3. Cách lọc trước khi chọn ở T-004

Áp dụng cùng các câu hỏi cho từng use case: (1) sự kiện nghiệp vụ và người chịu trách nhiệm có rõ không; (2) có dữ liệu hợp lệ, gần camera thực tế, gồm người đúng/người sai/người ngoài danh sách không; (3) có thể tách đăng ký, hiệu chỉnh, kiểm tra để tránh rò rỉ không; (4) có baseline và một điểm yếu đo được không; (5) demo mobile có phản ánh camera nghiên cứu không; (6) công sức ghi nhãn, tính toán và xử lý ngoại lệ có vừa sức không.

**Ưu tiên kiểm tra tiếp, chưa chốt:** G có nghiệp vụ theo phòng/ca rõ, điều kiện cửa phòng thi đặc trưng và vai trò thật cho camera mobile; Quốc An ưu tiên luồng khai báo mã rồi xác minh 1:1. B sát camera điện thoại nhưng chưa tự chứng minh đang ở lớp; C có sự kiện vào/ra rõ; D có câu hỏi về quyết định từ nhiều khung hình. A cần dữ liệu lớp học thực, E có yêu cầu an toàn cao, F phụ thuộc dữ liệu khách. Thứ tự này là giả thuyết của Quốc An, có thể đổi sau khi kiểm chứng và trao đổi với Minh Hy.

### Đề nghị cổng chốt nghiệp vụ trước T-005/T-006

Sau khi T-002 và T-003 được trình bày, T-004 chọn một use case chính và luồng xác minh cơ bản. Trước khi bắt đầu khảo sát kỹ thuật sâu, nhóm cần một lần rà soát nghiệp vụ riêng trong T-004 hoặc một task kế cận nếu khối lượng lớn. Đầu ra là mô tả nghiệp vụ được cả hai thống nhất, không chỉ một câu tên đề tài.

Tối thiểu phải có: dữ liệu đầu vào và người chịu trách nhiệm xác thực ảnh đăng ký; phiên bản danh sách theo kỳ thi/phòng/ca; luồng một lượt từ xếp hàng đến ghi nhận; các trạng thái kết quả; ai có quyền quyết định khi máy không chắc; quy tắc sai phòng, trùng lượt, đến muộn, ảnh kém, khẩu trang, người ngoài danh sách, nghi giả mạo, đổi phòng, mất mạng và hỏng thiết bị; nhật ký và cách sửa sai. Với từng ngoại lệ, ghi điều kiện phát hiện, hành động của hệ thống, người xử lý và bằng chứng lưu lại. Những điểm phụ thuộc quy chế kỳ thi hoặc ý kiến thầy phải được đánh dấu chờ xác nhận.

Chốt ở cổng này **có khai báo danh tính trước hay không**, vì nó quyết định 1:1 hay 1:N, dữ liệu và metric. Chưa cần chốt cách nhập/quét mã, model, ngưỡng hay thuật toán tối ưu; đó là lựa chọn triển khai và khảo sát sau.

## 4. Cầu nối sang T-005/T-006

Sau khi T-004 chọn một use case, mỗi hướng kỹ thuật được mô tả như một **gói kiểm chứng**: điều kiện camera → dữ liệu/quyền dùng → tập đăng ký, hiệu chỉnh và kiểm tra → pipeline gốc → 1–2 baseline → điểm lỗi quan sát được → lựa chọn cải thiện → metric/chi phí → khả năng chạy mobile. Không cần thử mọi tích Descartes dataset × model × pipeline × thuật toán.

Nhóm hướng cải thiện cần khảo sát gồm phát hiện/căn chỉnh dưới điều kiện khó, ảnh/mẫu đăng ký, đặc trưng nhận dạng, ngưỡng quyết định, gộp nhiều khung hình, và tốc độ/kích thước mobile. Mỗi hướng có thể cần dữ liệu hoặc model riêng để xem xét; số liệu từ các tập khác nhau không so trực tiếp. Trong một phép thử baseline–proposed, giữ cùng dữ liệu, split, metric và điều kiện đo. Nếu thay nhiều phần, đo tác động từng phần.

[NIST đánh giá xác minh 1:1](https://pages.nist.gov/frvt/html/frvt11.html) và [nhận diện 1:N](https://pages.nist.gov/frvt/html/frvt1N.html) theo các loại lỗi khác nhau, nên metric phải theo nghiệp vụ. [MobileFaceNets](https://arxiv.org/abs/1804.07573) là ví dụ về hướng model gọn, chưa phải lựa chọn của nhóm. Quyền dùng mã nguồn, trọng số và dataset phải kiểm tra riêng: [InsightFace nêu giới hạn của trọng số phát hành](https://github.com/deepinsight/insightface/blob/master/python-package/docs/model_zoo.md); [300-W nêu điều kiện dùng dữ liệu nghiên cứu](https://ibug.doc.ic.ac.uk/resources/300-W/). Các nguồn này chỉ là điểm bắt đầu cho khảo sát kỹ thuật.

## 5. Câu hỏi cần trao đổi

- Bối cảnh nào nhóm có thể quan sát hoặc mô phỏng trung thực, và ai có quyền cung cấp dữ liệu?
- Nếu không nhận ra mặt, có được ghi vắng mặt/từ chối không, hay phải chuyển xử lý thủ công?
- Tác vụ chính là 1:1, 1:N danh sách đóng, hay 1:N có người ngoài danh sách?
- Mobile là camera thu ảnh chính, thiết bị suy luận, hay giao diện demo?
- Lỗi chấp nhận sai và từ chối sai nào quan trọng nhất? Điều gì cần thầy xác nhận?

Sau khi Quốc An và Minh Hy trao đổi, T-004 mới ghi một use case chính và quyết định của nhóm; câu hỏi chưa được thầy xác nhận tiếp tục ở docs/00-project/questions.md.
