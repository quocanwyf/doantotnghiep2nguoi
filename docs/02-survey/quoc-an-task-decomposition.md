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

| Stage | Vấn đề và loại task | Input → output | ML bắt buộc? | Loại giải pháp cần khảo sát |
|---|---|---|---|---|
| S0. Chuẩn bị hồ sơ | Dữ liệu nghiệp vụ, enrollment/reference integrity | roster + ảnh → hồ sơ theo mã | Không | Kiểm tra schema, duy nhất mã, phiên bản roster, chất lượng ảnh tối thiểu; nếu ảnh thiếu/sai thì chuyển thủ công |
| S1. Nhận claim và truy xuất | Database lookup, transaction state | mã + phòng/ca hiện hành → đúng một hồ sơ hoặc lỗi | Không | Tra cứu có kiểm tra mã, quyền truy cập, xử lý mã lạ và race condition |
| S2. Thu hình | Camera acquisition và giới hạn thời gian | camera + hướng dẫn → cửa sổ frame có timestamp | Không bắt buộc | Vùng đứng, exposure/focus, timeout, retry, đồng bộ thời gian; không giả định mọi frame đều dùng được |
| S3. Tìm mặt và vị trí đặc trưng | Face detection/localization; có thể dự đoán 5 landmarks cùng lượt | frame → nhiều bbox, landmark, confidence | Có thể dùng detector học máy | Face-specific detector có landmark; so với phương án detector + landmark riêng nếu cần |
| S4. Chọn đúng người | Target selection, có thể thêm temporal association/tracking | tập mặt qua các frame + vùng đứng → một track mục tiêu hoặc ambiguous | Chưa chắc | Spatial gate, kích thước/khoảng cách, ổn định qua frame, tracking đơn giản; từ chối khi hai người tranh vùng |
| S5. Chọn ảnh đạt chất lượng | Quality assessment/selection | track mục tiêu → frame hợp lệ hoặc retry | Không bắt buộc | Quy tắc blur, sáng, kích thước, pose/che; learned quality chỉ xét khi quy tắc đơn giản không đủ |
| S6. Chuẩn hóa mặt | Geometric alignment/preprocessing | bbox + landmarks + ảnh → ảnh mặt cùng quy ước với encoder | Không nếu đã có landmark | Similarity transform/crop; landmark model riêng là nhánh có điều kiện |
| S7. Tạo biểu diễn | Face representation/embedding | ảnh tham chiếu và ảnh probe → vector đặc trưng | Có, nếu dùng deep face encoder | Mạng trích đặc trưng đã học trên danh tính rộng; trọng số và preprocessing phải định danh cụ thể |
| S8. So khớp và ra quyết định thị giác | 1:1 verification + calibration | hai embedding/điểm → match, non-match hoặc uncertain | Không nhất thiết có model mới | Similarity/distance, ngưỡng trên development set, vùng retry/manual, không dùng ngưỡng của model khác |
| S9. Kiểm tra điều kiện thi | Deterministic business validation | hồ sơ + phòng/ca/giờ + match → điều kiện hợp lệ/ngoại lệ | Không | Quy tắc cấu hình theo kỳ thi; sai phòng/ca, đến muộn, eligibility, duplicate |
| S10. Ghi nhận và đối soát | Database transaction/audit | quyết định + trạng thái trước → check-in hoặc nhật ký ngoại lệ | Không | Ghi atomically/idempotent, audit ai xử lý và lúc nào, đối soát có mặt/vắng |
| S11. Chống trình ảnh/video giả | Presentation Attack Detection (PAD), **ngoài đóng góp nhận diện chính hiện tại** | tín hiệu thu → nghi tấn công / không chắc | Có thể cần ML/phần cứng riêng | Phân tích như task độc lập nếu tích hợp; không suy từ verification score rằng ảnh là người sống |

**Không ép mọi stage thành một model.** S3 và S7 là hai nhóm model lõi có thể cần benchmark; S4–S6, S8 có thể bắt đầu bằng thuật toán xác định. S9–S10 là phần mềm. Nếu detector đã trả landmark, S3 và phần ước lượng landmark của S6 được gộp thành một lần suy luận; nếu chỉ dùng ảnh tĩnh, tracking của S4 không cần. PAD S11 là mô-đun sản phẩm tùy phạm vi, không nằm trong mục tiêu tối ưu nhận diện T-005.

## 4. Giao diện giữa các stage và điều kiện lỗi

- **S0–S1:** không có hồ sơ, trùng mã hoặc ảnh tham chiếu sai/không đọc được → dừng xác minh và chuyển người phụ trách; không dùng ảnh người khác làm fallback.
- **S2–S4:** không tìm thấy mặt, tìm nhiều mặt nhưng không xác định chắc người đang làm thủ tục → retry/manual. Không mặc định lấy mặt lớn nhất hoặc rõ nhất trong cả hành lang.
- **S5–S7:** ảnh quá mờ/che, landmark sai, preprocessing không tương thích trọng số → retry/manual hoặc lỗi kỹ thuật; tách lỗi này khỏi false non-match của encoder.
- **S8:** similarity không đủ chắc → vùng uncertain; không tự kết luận thí sinh không được thi chỉ vì score thấp.
- **S9–S10:** match mặt không tự cấp quyền vào phòng; nghiệp vụ phải kiểm tra riêng và tránh hai thiết bị ghi hai lượt cùng lúc.

Để đo pipeline đầu-cuối cần nhãn của **người thực sự làm thủ tục** và claim tương ứng. Dataset chỉ có các bbox mặt mà không có nhãn người mục tiêu không thể đo S4 hay giao dịch cuối. Phần [khảo sát dataset](quoc-an-datasets.md) sẽ đánh dấu chỗ thiếu loại nhãn này thay vì tự gán rằng đã giải quyết.

## 5. Research pipeline, khác runtime pipeline

Bài toán → bản đồ S0–S11 → yêu cầu dữ liệu theo task → khảo sát nguồn dữ liệu → shortlist có điều kiện → họ phương pháp theo task → lọc candidate → thí nghiệm baseline → phân tích lỗi theo stage → xác định bottleneck thực nghiệm → mới chọn biến/objective/thuật toán tối ưu → ablation → đánh giá cuối. **Benchmark và error analysis là hoạt động nghiên cứu**, không phải model chạy ở cửa. Kết quả của T-005 là thiết kế đủ cụ thể để chạy baseline và nêu các quyết định còn mở; không có số liệu trước khi thí nghiệm.

## 6. Điều cần chốt trước khi gọi đây là pipeline triển khai

Loại kỳ thi minh họa và quy tắc ngoại lệ; ảnh tham chiếu tối thiểu; một hay nhiều ảnh mỗi hồ sơ; smartphone có chạy suy luận tại chỗ hay chỉ thu ảnh; mục tiêu latency/RAM/dung lượng; có bắt buộc train/fine-tune hay không; mức tự động hóa có thể demo. Các chi tiết này hiện là **câu hỏi mở**, không được dùng làm giả định đã được thầy duyệt. Với kỳ thi có quy chế giám thị đối chiếu trực tiếp, kết quả prototype chỉ hỗ trợ thao tác trong phạm vi được phép.
