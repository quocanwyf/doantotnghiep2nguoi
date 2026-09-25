# T-005 / Quốc An — Phân rã bài toán và xác định task

**Ngày khảo sát:** 2026-09-25. **Trạng thái:** thiết kế nghiên cứu, chưa chốt dataset, model, pipeline triển khai hay optimization. Tài liệu này chỉ xuất phát từ [bối cảnh phòng thi T-002](../01-problem/quoc-an-proposal.md), yêu cầu chức năng Quốc An bổ sung và [định hướng dự án](../00-project/brief.md). Đọc tiếp [khảo sát dữ liệu](quoc-an-datasets.md), [khảo sát phương pháp/model](quoc-an-models.md), [thiết kế thí nghiệm](quoc-an-experiments.md) theo thứ tự.

## 1. Business problem và ranh giới đồ án

Trước ca thi, đơn vị tổ chức có một mã thí sinh duy nhất, ảnh đăng ký, hồ sơ, phòng, ca/môn, thời gian và trạng thái đủ điều kiện. Ở cửa, một người khai báo mã. Hệ thống cần xác minh **người đang làm thủ tục** có cùng danh tính với ảnh tham chiếu của hồ sơ đó không, rồi kiểm tra quyền vào đúng phòng/ca/giờ và tình trạng đã check-in. Kết quả có thể là tiếp tục, yêu cầu thử lại hoặc chuyển người phụ trách. Lượt được ghi nhận cùng lịch sử xử lý để đối soát người đến/vắng.

Mục tiêu sản phẩm là giảm tải thao tác kiểm tra thường lệ tại cửa, sau này có thể chạy trên smartphone hoặc edge device. Đồ án dùng **dataset công khai** để nghiên cứu phần thị giác và hồ sơ giả lập để kiểm thử nghiệp vụ; chưa có dữ liệu thí sinh thật hay phép đo giảm nhân sự ngoài thực tế. Ràng buộc mobile hiện là định hướng, **chưa có điện thoại đích, ngưỡng độ trễ, RAM, dung lượng hay chế độ offline được chốt**. Không biến các giá trị chưa chốt thành tiêu chí loại model cứng.

## 2. Problem formulation: hệ thống cần xác minh cái gì?

Khi thí sinh khai báo mã C, hệ thống truy xuất một ảnh tham chiếu R(C) và thu ảnh/video Q của người đứng trước camera. Câu hỏi thị giác là **face verification 1:1 với cả claim đúng và claim giả**: quyết định liệu R(C) và mặt mục tiêu trong Q có cùng identity không. Cặp khác người phải được phép trả về “không khớp”. Mã C chỉ chọn ảnh để so, không phải bằng chứng danh tính.

**Face identification 1:N** sẽ hỏi “người này là ai trong cả danh sách?” khi chưa có claim; không phải luồng đã chọn. **Closed-set classification** với một output class cho từng thí sinh càng không phù hợp: danh sách/phòng thay đổi theo kỳ thi, người ngoài danh sách phải bị từ chối và không thể train lại classifier sau mỗi lần thêm hồ sơ. Việc huấn luyện một face encoder trên các identity của tập train có thể dùng classification/margin loss, nhưng đó là **training objective**, không phải classifier thí sinh ở runtime. Metric learning cũng thuộc cách học embedding, không phải một stage suy luận riêng.

## 3. Product/runtime pipeline ở mức task, chưa gắn model

**Trước ca:** nhập và kiểm tra roster/ảnh tham chiếu → gắn mã, phòng, ca, quyền dự thi → chuẩn bị thiết bị và phiên bản dữ liệu. **Mỗi lượt:** nhận claim → truy hồ sơ → thu một cửa sổ ảnh có hướng dẫn vị trí → tìm mặt/điểm mặt → liên kết đúng người đang làm thủ tục và kiểm tra chất lượng → chuẩn hóa ảnh mặt → tạo biểu diễn → so với ảnh tham chiếu → quyết định xác minh hoặc retry/manual → kiểm tra điều kiện thi → ghi check-in và audit atomically. **Sau ca:** đối soát có mặt/vắng/ngoại lệ.

| Stage | Việc cần làm | Input → output | Có cần model không? | Loại model/thuật toán |
|---|---|---|---|---|
| S0. **Enrollment / reference preparation** | Kiểm tra roster, mã duy nhất và ảnh đăng ký trước ca; gắn đúng ảnh với hồ sơ. | danh sách + ảnh → reference hợp lệ hoặc ngoại lệ | Không bắt buộc; nếu kiểm tra mặt tự động thì dùng lại S3/S5 | Database validation, kiểm tra ảnh; tạo reference embedding bằng cùng S7 khi pipeline đã chọn |
| S1. **Candidate lookup** | Nhận mã dự thi đã khai báo và lấy đúng một hồ sơ; mã chỉ là claim, không chứng minh danh tính. | mã + kỳ thi → một hồ sơ hoặc lỗi | Không | Database query, kiểm tra quyền và phiên bản roster |
| S2. **Camera acquisition** | Thu frame của từng lượt, giới hạn thời gian và hướng dẫn người làm thủ tục đứng trong vùng kiểm tra. | camera → frame/chuỗi frame có timestamp | Không | Camera API, focus/exposure, timeout và retry |
| S3. **Face detection / landmark localization** | Tìm mọi khuôn mặt trong frame và vị trí điểm mặt cần cho alignment. | frame → bbox, confidence, landmarks của từng mặt | Có, thông thường | Face detector có landmark; hoặc detector + landmark estimator riêng |
| S4. **Subject selection** | Xác định mặt của **người đang làm thủ tục** giữa các mặt nhìn thấy; không tự lấy người nền. | các bbox/track + vùng đứng → một subject hoặc ambiguous | Có thể | ROI/rule, liên kết qua frame hoặc tracking nếu có dữ liệu và nhu cầu |
| S5. **Face quality check** | Phát hiện ảnh mờ, mặt quá nhỏ, lệch góc, thiếu sáng/che; chọn frame dùng được hoặc yêu cầu chụp lại. | mặt/track → frame hợp lệ hoặc retry | Có thể | Rule đo blur, kích thước, pose, sáng; face-quality model nếu rule chưa đủ |
| S6. **Face alignment** | Đưa mắt/mũi/miệng về template đúng với encoder, rồi crop/normalize ảnh mặt. | ảnh + bbox/landmarks → face crop chuẩn | Không cần model riêng nếu S3 đã có landmarks | Landmark + geometric transform; estimator riêng chỉ khi có bằng chứng cần |
| S7. **Feature extraction / face embedding** | Biến ảnh đăng ký và ảnh camera thành embedding có thể so danh tính mới. | hai face crop → hai vector đặc trưng | Có | Pretrained face encoder; architecture/weight/preprocessing khảo sát riêng |
| S8a. **Verification 1:1** | So embedding camera với embedding của **một** hồ sơ đã khai báo; tính score cùng/khác người. | hai embedding → similarity/distance score | Không cần classifier thí sinh riêng | Cosine similarity hoặc distance phù hợp encoder |
| S8b. **Decision policy** | Chuyển score thành match, non-match hoặc uncertain để retry/chuyển người phụ trách. | score + quality/status → quyết định có lý do | Không nhất thiết | Threshold được calibrate trên development set; có thể dùng hai ngưỡng |
| S9. **Business validation** | Kiểm tra đúng phòng, ca/môn, giờ, eligibility và lượt check-in trước. | hồ sơ + cấu hình ca + quyết định mặt → hợp lệ/ngoại lệ | Không | Rule/database; quy tắc do kỳ thi xác định |
| S10. **Attendance / audit logging** | Ghi check-in, retry hoặc manual override; tránh ghi trùng và cho phép đối soát. | kết quả + trạng thái trước → trạng thái mới + audit log | Không | Backend transaction, idempotency và nhật ký |
| S11. **Presentation Attack Detection (PAD, optional)** | Nếu tích hợp, phát hiện trình ảnh/video hoặc tín hiệu giả mạo; không suy từ score verification. | tín hiệu camera → bona fide/attack/uncertain | Có thể cần model hoặc phần cứng riêng | Presentation Attack Detection; dataset và metric riêng |

**Tên stage dùng thuật ngữ kỹ thuật; phần mô tả tiếng Việt cho biết chính xác thao tác của stage.** S0 và S2 là bước vận hành cần có dù không phải bài toán ML. S8a tính bằng chứng so khớp, còn S8b áp chính sách quyết định; tách chúng để không gọi threshold là một recognition model.

**Không ép mọi stage thành một model.** S3 và S7 là hai nhóm model lõi có thể cần benchmark; S4–S6 và S8a–S8b có thể bắt đầu bằng thuật toán xác định. S9–S10 là phần mềm. Nếu detector đã trả landmark, S3 và phần ước lượng landmark của S6 được gộp thành một lần suy luận; nếu chỉ dùng ảnh tĩnh, tracking của S4 không cần. PAD S11 là mô-đun sản phẩm tùy phạm vi, không nằm trong mục tiêu tối ưu nhận diện T-005. “Liveness” thường được dùng khi nói về người thật trước camera, nhưng kiểm thử chống ảnh/video giả trong tài liệu này gọi chính xác là **Presentation Attack Detection**.

## 4. Giao diện giữa các stage và điều kiện lỗi

- **S0–S1:** không có hồ sơ, trùng mã hoặc ảnh tham chiếu sai/không đọc được → dừng xác minh và chuyển người phụ trách; không dùng ảnh người khác làm fallback.
- **S2–S4:** không tìm thấy mặt, tìm nhiều mặt nhưng không xác định chắc người đang làm thủ tục → retry/manual. Không mặc định lấy mặt lớn nhất hoặc rõ nhất trong cả hành lang.
- **S5–S7:** ảnh quá mờ/che, landmark sai, preprocessing không tương thích trọng số → retry/manual hoặc lỗi kỹ thuật; tách lỗi này khỏi false non-match của encoder.
- **S8a–S8b:** similarity không đủ chắc → vùng uncertain; không tự kết luận thí sinh không được thi chỉ vì score thấp.
- **S9–S10:** match mặt không tự cấp quyền vào phòng; nghiệp vụ phải kiểm tra riêng và tránh hai thiết bị ghi hai lượt cùng lúc.

Để đo pipeline đầu-cuối cần nhãn của **người thực sự làm thủ tục** và claim tương ứng. Dataset chỉ có các bbox mặt mà không có nhãn người mục tiêu không thể đo S4 hay giao dịch cuối. Phần [khảo sát dataset](quoc-an-datasets.md) sẽ đánh dấu chỗ thiếu loại nhãn này thay vì tự gán rằng đã giải quyết.

## 5. Research pipeline, khác runtime pipeline

Bài toán → bản đồ S0–S11 (S8 tách thành S8a và S8b) → yêu cầu dữ liệu theo task → khảo sát nguồn dữ liệu → shortlist có điều kiện → họ phương pháp theo task → lọc candidate → thí nghiệm baseline → phân tích lỗi theo stage → xác định bottleneck thực nghiệm → mới chọn biến/objective/thuật toán tối ưu → ablation → đánh giá cuối. **Benchmark và error analysis là hoạt động nghiên cứu**, không phải model chạy ở cửa. Kết quả của T-005 là thiết kế đủ cụ thể để chạy baseline và nêu các quyết định còn mở; không có số liệu trước khi thí nghiệm.

## 6. Điều cần chốt trước khi gọi đây là pipeline triển khai

Loại kỳ thi minh họa và quy tắc ngoại lệ; ảnh tham chiếu tối thiểu; một hay nhiều ảnh mỗi hồ sơ; smartphone có chạy suy luận tại chỗ hay chỉ thu ảnh; mục tiêu latency/RAM/dung lượng; có bắt buộc train/fine-tune hay không; mức tự động hóa có thể demo. Các chi tiết này hiện là **câu hỏi mở**, không được dùng làm giả định đã được thầy duyệt. Với kỳ thi có quy chế giám thị đối chiếu trực tiếp, kết quả prototype chỉ hỗ trợ thao tác trong phạm vi được phép.
