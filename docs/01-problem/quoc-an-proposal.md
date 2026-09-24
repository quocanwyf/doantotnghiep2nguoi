# T-002 — Đề xuất của Quốc An: xác thực thí sinh tại cửa phòng thi

**Trạng thái:** phương án Quốc An chủ động đề xuất để so sánh với đề xuất độc lập T-003 của Minh Hy. Chưa phải lựa chọn chính thức của nhóm ở T-004; chưa chọn dataset, model hoặc thuật toán tối ưu.

## 1. Vấn đề và giá trị nghiệp vụ

Trước một kỳ thi, đơn vị tổ chức đã có danh sách thí sinh theo điểm thi, phòng, môn và ca, cùng ảnh đăng ký. Tại cửa phòng, giám thị phải nhận diện người đến, đối chiếu hồ sơ/giấy tờ, kiểm tra đúng phòng và thời điểm, rồi ghi nhận lượt vào. Nhiều thí sinh đến gần cùng lúc làm khâu này dễ ùn hàng, nhập nhầm hoặc khó rà soát khi phát sinh tranh chấp. Phòng thi có thể gồm thí sinh từ nhiều lớp, trường hoặc nhóm; đơn vị nghiệp vụ là **phòng + ca thi**, không phải lớp học.

Quốc An đề xuất một thiết bị camera đặt trước cửa, ban đầu là điện thoại, để **hỗ trợ giám thị xác minh danh tính và ghi nhận lượt làm thủ tục**. Hệ thống phải trả lời: người đang làm thủ tục có khớp hồ sơ đã khai báo, được xếp vào đúng phòng/ca và chưa có lượt ghi nhận trùng không? Kết quả không chắc chắn chuyển cho người có thẩm quyền xử lý. Giá trị dự kiến là thao tác tra cứu nhanh hơn, ít nhầm phòng/ca hơn, danh sách có mặt cập nhật rõ hơn và có nhật ký để đối soát.

Với kỳ thi tốt nghiệp THPT theo quy chế hiện được công bố, giám thị vẫn có nhiệm vụ gọi tên, đối chiếu danh sách ảnh và giấy tờ tùy thân, rồi tiếp tục kiểm tra trong phòng. Vì vậy đề xuất này **không mặc nhiên bỏ bước kiểm tra do quy chế yêu cầu**; mức tự động hóa phải được xác nhận theo từng loại kỳ thi và đơn vị tổ chức. Nguồn: [Quy chế thi của Bộ GD&ĐT, phần nhiệm vụ giám thị](https://vqa.moet.gov.vn/uploads/news/2024_12/final-quy-che-thi-tot-nghiep-thpt.pdf).

## 2. Bối cảnh sử dụng và người tham gia

- **Đơn vị tổ chức thi:** cung cấp, kiểm tra và chốt danh sách thí sinh; xác định phòng, ca, thời gian và người có quyền xử lý ngoại lệ.
- **Giám thị tại cửa/phòng:** vận hành thiết bị, xem kết quả, kiểm tra giấy tờ và quyết định theo quy chế. Người có thẩm quyền cao hơn xử lý trường hợp cần thay đổi danh sách hoặc cho phép ngoại lệ.
- **Thí sinh:** xếp hàng và từng người bước vào vùng làm thủ tục, khai báo mã dự thi, nhìn vào camera, nhận hướng dẫn khi cần chụp lại.
- **Thiết bị:** điện thoại đặt cố định ở cửa phòng trong bản đầu; hành lang có thể đông và có người khác trong nền ảnh, nhưng mỗi lượt chỉ một thí sinh đứng trong vùng kiểm tra. Một hướng sản phẩm về sau là thay bằng thiết bị edge nếu quy trình và kết quả đo chứng minh phù hợp.

## 3. Luồng nghiệp vụ Quốc An đề xuất

**Trước ca thi:** đơn vị tổ chức nhập danh sách đã xác thực gồm mã thí sinh duy nhất, ảnh đăng ký có nguồn rõ, phòng, ca/môn, thời gian, tình trạng đủ điều kiện và thông tin cần hiển thị cho giám thị. Chốt phiên bản danh sách; giám thị chọn đúng phòng/ca trên thiết bị, kiểm tra camera và tình trạng dữ liệu.

**Mỗi lượt tại cửa:**

1. Thí sinh **khai báo mã dự thi trước**. Hệ thống lấy đúng một hồ sơ trong kỳ thi. Việc nhập số báo danh, quét mã trên giấy báo dự thi hay phương tiện khác chưa cần quyết ở T-002; mã chỉ dùng để tìm hồ sơ, không tự chứng minh người cầm mã là chủ hồ sơ.
2. Camera thu người đang đứng trong vùng làm thủ tục. Nếu có người khác ở nền, hệ thống phải chọn đúng người trong vùng; nếu nhiều mặt cùng chen vào vùng hoặc ảnh kém thì hướng dẫn làm lại.
3. Hệ thống đối chiếu mặt người này với ảnh đăng ký của hồ sơ đã khai báo: **xác minh 1:1**. Đồng thời kiểm tra đúng phòng, đúng ca, khoảng thời gian cho phép và tình trạng đã ghi nhận hay chưa.
4. Hiển thị một kết quả có lý do để giám thị quyết định: phù hợp để tiếp tục làm thủ tục; cần chụp lại; hoặc cần xử lý thủ công vì không khớp, sai phòng/ca, trùng lượt, quá giờ hay dữ liệu bất thường. Một điểm nhận dạng thấp không tự tước quyền dự thi của người hợp lệ.
5. Ghi lại kết quả lượt, thời điểm, người xử lý và lý do nếu có sửa/ghi nhận ngoại lệ; sau ca cho phép đối soát danh sách đã đến, vắng và các trường hợp cần xác minh.

**Sau ca thi:** người phụ trách đối soát với danh sách phòng và biên bản giám thị, xử lý sai lệch, lưu hoặc xóa dữ liệu theo quy trình đã được đơn vị tổ chức phê duyệt. Việc thiết bị tự mở cửa, tự cho vào không cần giám thị, hay thay hoàn toàn kiểm tra giấy tờ **không thuộc phạm vi đề xuất ban đầu**.

## 4. Điều kiện cần, điều muốn và ngoại lệ phải đặc tả

**Điều kiện cần:** danh sách/ảnh đăng ký đáng tin và được phép dùng; mã trỏ đúng một hồ sơ; camera chọn đúng người đang làm thủ tục dù có người xung quanh; xác minh 1:1; kiểm tra phòng/ca/trạng thái; có lối xử lý khi máy không chắc; ghi vết và sửa sai. Chưa thể coi nhận dạng mặt là bằng chứng đủ cho việc người trước camera là người thật hoặc giấy tờ họ xuất trình là thật.

**Điều muốn sau khi phần cốt lõi chạy được:** giảm thời gian mỗi lượt, hoạt động khi mạng không ổn định, triển khai nhiều phòng bằng điện thoại rồi thiết bị edge, và giảm tỷ lệ phải kiểm tra thủ công mà không làm tăng rủi ro nhận nhầm. Mức tự động hóa sẽ phụ thuộc quy chế của kỳ thi.

Các ngoại lệ phải được bàn kỹ: sai phòng; sai ca/môn; quá giờ; mã không có trong danh sách; hồ sơ đổi phòng phút cuối; lượt vào trùng hoặc thí sinh quay lại; ảnh đăng ký sai/cũ; ảnh thu mờ, ngược sáng, mặt nghiêng, khẩu trang; có nhiều mặt trong vùng; người ngoài danh sách; nghi dùng ảnh/video giả mạo; thí sinh không có giấy tờ; mất mạng, lệch giờ hoặc hỏng thiết bị; nhu cầu hỗ trợ đặc biệt. Chưa tự đặt quy tắc cho phép/từ chối từng trường hợp ở T-002.

## 5. Bài toán kỹ thuật suy ra từ nghiệp vụ

Bài toán nhận dạng chính là **1:1 có khai báo danh tính**: ảnh thu tại cửa so với ảnh đăng ký của một hồ sơ. Phần nghiệp vụ còn phải kiểm tra phòng/ca, thời gian và trạng thái lượt vào. Trong trường hợp có người xung quanh, phát hiện mặt nào thuộc lượt đang xử lý là một vấn đề đầu vào riêng. Không dùng mặt “rõ nhất” trong cả khung hình làm mặc định.

Pipeline gốc ở mức khái niệm: khai báo mã → tìm hồ sơ → thu và chọn mặt người trong vùng → kiểm tra chất lượng/căn chỉnh → tạo đặc trưng → so với ảnh đăng ký → quyết định mức tin cậy → kiểm tra điều kiện phòng/ca/trạng thái → hiển thị cho giám thị. Đây là khung để khảo sát về sau, chưa chọn thành phần, model hay thuật toán.

Các điểm có thể chưa tốt chỉ là **giả thuyết cần kiểm chứng**: chọn nhầm người trong nền; ảnh ở cửa kém hơn ảnh đăng ký; sai từ chối khi đeo khẩu trang/ánh sáng xấu; sai chấp nhận khi khuôn mặt giống nhau; chờ lâu khi hàng đông; ảnh/video giả mạo. T-005/T-006 sẽ khảo sát dữ liệu, baseline, đo lỗi thực tế, rồi mới chọn một hoặc vài điểm có cơ sở để cải thiện. Nếu thay nhiều thành phần phải tách tác động từng thay đổi.

## 6. Tiêu chí để đánh giá tính khả thi ở T-004

- Có quyền dùng ảnh đăng ký và dữ liệu thử nghiệm gần với cửa phòng thi, gồm nhiều lần chụp mỗi người, điều kiện sáng/đông người khác nhau, người đúng và sai hồ sơ không?
- Có thể xác định rõ giám thị/người có thẩm quyền xử lý từng trạng thái và đối soát kết quả không?
- Có thể thử toàn bộ lượt làm thủ tục, không chỉ độ chính xác trên ảnh mặt đã cắt sẵn không?
- Có thể đo hai loại lỗi quan trọng — nhận nhầm người và bỏ sót người hợp lệ — cùng tỷ lệ chuyển xử lý thủ công, thời gian mỗi lượt và lỗi ở cấp quyết định vào đúng phòng/ca không?
- Có thể demo bằng điện thoại đặt tại cửa với cùng điều kiện camera trong nghiên cứu không?
- Có thể thử nghiệm trong phạm vi đồ án mà không tuyên bố thay thế các bước giám thị bắt buộc theo quy chế không?

Các bối cảnh đã xem trước đó — điểm danh bằng điện thoại cá nhân, kiosk nhân viên, camera toàn lớp, phòng họp, cửa tòa nhà và quầy lễ tân — là đối chiếu để lý giải lựa chọn. Quốc An **đề xuất bối cảnh phòng thi làm phương án chính** vì sự kiện cần quyết định rõ, danh sách theo phòng/ca có trước, camera mobile có vai trò thật và điều kiện hành lang tạo vấn đề nhận dạng cần kiểm chứng. Đây chưa phải kết luận của nhóm trước T-004.

## 7. Checkpoint nghiệp vụ trước khảo sát kỹ thuật sâu

T-004 cần so sánh đề xuất của Quốc An với T-003 của Minh Hy và chọn một use case. Nếu nhóm chọn phòng thi, Quốc An đề nghị một **cổng đặc tả nghiệp vụ riêng sau lựa chọn và trước T-005/T-006**; có thể đặt thành task trên Sheet nếu khối lượng lớn. Cổng này phải có sơ đồ luồng lượt vào, danh mục trạng thái và bảng ngoại lệ. Với mỗi ngoại lệ, ghi điều kiện phát hiện, hành động của hệ thống, ai có quyền quyết định, thông tin nào cần lưu và cách sửa sai. Hai người phải thống nhất; các điểm phụ thuộc quy chế hoặc ý kiến thầy phải được đánh dấu chờ xác nhận.

Ở T-002 đã xác định **ưu tiên có khai báo mã rồi xác minh 1:1**. Tại cổng nghiệp vụ mới chốt cách khai báo, quy tắc đúng/sai phòng/ca, đến muộn, trùng lượt, kiểm tra giấy tờ, mức xử lý nghi giả mạo và luồng dự phòng. T-005/T-006 mới chọn dữ liệu, baseline, metric kỹ thuật, model và hướng tối ưu. Không dùng việc thử model để thay cho việc thống nhất quy trình nghiệp vụ.

## 8. Câu hỏi mở để trao đổi với Minh Hy và thầy

1. Kỳ thi mục tiêu để làm đồ án/pilot là kỳ thi nào? Quy chế cụ thể cho phép hệ thống hỗ trợ giám thị ở bước nào?
2. Ai có quyền cung cấp ảnh đăng ký; ảnh đó được xác thực khi đăng ký ra sao; có đủ ảnh qua nhiều thời điểm/điều kiện để thử không?
3. Ai là người quyết định cuối cùng khi hệ thống báo không khớp, đến muộn hoặc nghi giả mạo?
4. Mục tiêu tối thiểu là hỗ trợ kiểm tra ở cửa hay tự động cho vào không cần người? Quốc An đề xuất bắt đầu bằng hỗ trợ giám thị.
5. Nếu không có dữ liệu từ kỳ thi thật, nhóm có thể mô phỏng luồng tại cửa với người tham gia đồng ý và công bố giới hạn kết luận thế nào?
6. Mobile chỉ là thiết bị thu ảnh hay phải chạy suy luận tại chỗ/offline? Cần quyết sau khi biết điều kiện vận hành và dữ liệu.
