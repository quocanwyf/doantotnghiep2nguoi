# T-008 — Yêu cầu nghiệp vụ cho thiết bị tại cửa phòng thi

**Trạng thái:** bản nghiệp vụ đang cùng Quốc An xây dựng; kỳ thi mục tiêu chưa chốt theo phản hồi ngày 2026-09-25. Cần nhóm rà soát các điểm chưa có nguồn. **Phạm vi đã chốt:** [D-001](../00-project/decisions/T-004-D-001-chon-bai-toan-cua-phong-thi.md) chọn bài toán T-002; [D-002](../00-project/decisions/T-007-D-002-chon-huong-khao-sat-t005.md) chọn khảo sát T-005. Tài liệu này xác định hệ thống cần làm gì trước khi khóa giao thức baseline T-010. Nó không chọn dataset, model, ngưỡng xác minh hoặc quy chế cho một kỳ thi cụ thể.

## 1. Vấn đề, mục tiêu và giới hạn bằng chứng

Theo [đề xuất T-002](T-002-quoc-an-proposal.md), khâu kiểm tra đầu vào hiện cần đối chiếu người đến với hồ sơ, phòng và ca, rồi ghi nhận. Việc này lặp lại ở nhiều cửa phòng; người đến muộn, nhầm phòng và trường hợp chưa đến cần được theo dõi để đối soát. Quy trình thực tế, số người bố trí và thời gian xử lý của **kỳ thi mục tiêu** chưa được khảo sát, nên đây là mô tả bối cảnh của nhóm, chưa phải số đo hiện trường.

Mục tiêu hệ thống là hỗ trợ thiết bị tại cửa xử lý **lượt thường lệ** và ghi nhận trạng thái có lý do, để giảm công đối chiếu lặp lại. Trường hợp không chắc hoặc trái quy tắc phải chuyển người có thẩm quyền. Chưa có pilot để kết luận giảm được bao nhiêu người hoặc thiết bị được thay bước kiểm tra bắt buộc nào.

## 2. Actor và quyền cần làm rõ

| Actor | Vai trò theo đề xuất đã chốt | Quyền cần xác nhận với kỳ thi mục tiêu |
|---|---|---|
| Đơn vị tổ chức | Cung cấp và chốt danh sách, ảnh tham chiếu, phân phòng, ca và mốc giờ | Ai phê duyệt phiên bản danh sách, quyền sửa và thời hạn lưu dữ liệu |
| Thí sinh | Khai báo mã cho lượt tại cửa, đứng trong vùng thu ảnh, nhận hướng dẫn thử lại | Cách khai báo mã và giấy tờ còn phải xuất trình |
| Giám thị/người phụ trách | Xem trạng thái, xử lý lượt được chuyển đến, đối soát sau ca | Ai được cho phép vào muộn, giải quyết nhầm phòng, ghi đè hoặc hủy lượt |
| Thiết bị/hệ thống | Tra hồ sơ theo mã; thu bằng chứng; trả trạng thái; ghi vết | Mức tự động ghi nhận và bước nào vẫn bắt buộc do người thực hiện |

Không gán cho thiết bị quyền quyết định thí sinh được dự thi, miễn kiểm tra giấy tờ hoặc mở cửa vật lý khi chưa có quy chế và người chốt quyền.

## 3. Đầu vào, đầu ra và ranh giới một lượt

**Trước ca:** cần có mã thí sinh duy nhất trong phạm vi kỳ thi, ảnh tham chiếu có nguồn và quyền dùng, phòng, ca/môn, điều kiện dự thi, thời gian áp dụng và phiên bản danh sách. Thiếu, trùng hoặc mâu thuẫn dữ liệu là ngoại lệ để người phụ trách sửa tại nguồn; thiết bị không tự điền một hồ sơ khác.

**Khi có người đến:** đầu vào của một lượt là mã người đó khai báo, phòng/ca mà thiết bị đang phục vụ, ảnh/chuỗi ảnh thu trong vùng làm thủ tục và thời điểm. Mã chỉ chọn **một hồ sơ để kiểm tra**, không chứng minh danh tính. Đầu ra phải tách được: bằng chứng cùng/khác người hoặc không đủ chắc; kết quả quy tắc phòng/ca/giờ/lượt trước; trạng thái hành động có lý do; và sự kiện ghi nhận nếu được phép. Tách này giúp truy lỗi là do ảnh, xác minh hay quy tắc nghiệp vụ.

**Sau ca:** đối soát những người đã ghi nhận, người còn chưa có lượt hợp lệ và mọi trường hợp chờ xử lý. “Chưa đến” là kết quả đối soát sau một mốc thời gian do kỳ thi xác định, không phải nhãn suy từ ảnh hay trạng thái gán ngay khi bắt đầu ca.

## 4. Yêu cầu có thể truy ngược

| ID | Yêu cầu nghiệp vụ | Vì sao cần | Bước sau sử dụng |
|---|---|---|---|
| BR-01 | Mỗi lượt gắn với đúng kỳ thi, phòng, ca và phiên bản danh sách. | Cùng một mã hoặc phòng có thể xuất hiện ở ngữ cảnh khác; cần tránh đối chiếu sai phiên. | T-010 định nghĩa fixture, protocol và kiểm thử rule. |
| BR-02 | Mã khai báo tra về đúng một hồ sơ hoặc lỗi rõ ràng; không xem mã là bằng chứng danh tính. | Người khác có thể biết hoặc cầm mã. | T-009 kiểm tra loại dữ liệu claim/reference; T-010 tạo cặp đúng và giả. |
| BR-03 | Bằng chứng khuôn mặt phải thuộc người đang làm thủ tục; ảnh kém, không có mặt hoặc nhiều người gây mơ hồ phải có đường thử lại/chuyển xử lý. | Hành lang có người nền; chọn nhầm mặt có thể dẫn tới chấp nhận sai. | T-009 kiểm tra nhãn người mục tiêu/domain gap; T-010 đo retry và lỗi theo stage. |
| BR-04 | So người trước camera với ảnh của hồ sơ đã khai báo theo bài toán 1:1; trả bằng chứng và mức không chắc thay vì ép mọi lượt thành chấp nhận/từ chối. | Mã chỉ là claim; nhận nhầm và từ chối nhầm có hậu quả khác nhau. | T-009 lọc dữ liệu/model candidate; T-010 định nghĩa FMR/FNMR và operating point. |
| BR-05 | Xác minh danh tính không thay kiểm tra phòng, ca, giờ, điều kiện dự thi và lượt đã ghi nhận. | Một người đúng danh tính vẫn có thể sai phòng/ca hoặc đến ngoài quy tắc. | T-010 kiểm thử rule/database độc lập với phần thị giác. |
| BR-06 | Trường hợp không chắc, sai quy tắc hoặc lỗi dữ liệu được chuyển cho người có quyền; điểm xác minh thấp không tự tước quyền dự thi. | Cần đường sửa sai và tránh hậu quả false reject không kiểm soát. | T-010 đo tỷ lệ retry/manual và định nghĩa tiêu chí xử lý. |
| BR-07 | Ghi nhận lượt phải tránh trùng và có vết thời điểm, kết quả, lý do, người/nguồn thực hiện và mọi sửa đổi. | Cần đối soát khi có nhiều lượt hoặc quyết định thủ công. | T-010/T-011 kiểm thử tính nhất quán, idempotency và audit. |
| BR-08 | Danh sách sau ca phân biệt người đã có lượt hợp lệ, đang chờ xử lý và người chưa có lượt sau mốc đối soát. | “Chưa đến” và “bị từ chối” không cùng nghĩa. | T-010 định nghĩa kịch bản nghiệp vụ và metric đầu-cuối. |

Các BR-03/04 nêu **năng lực cần có**, chưa chỉ định detector, encoder, threshold hoặc cách chọn người mục tiêu. [Phân rã T-005](../02-survey/T-005-quoc-an-task-decomposition.md) mới ánh xạ sang stage kỹ thuật S0–S10.

## 5. Đề xuất trạng thái và quy tắc chưa được xác nhận

Để viết fixture và giao diện, cần phân biệt ba lớp thông tin: **tình trạng hồ sơ trong danh sách**, **kết quả từng lần thử tại cửa**, và **trạng thái hiện diện sau ca**. Không ghi đè cả ba bằng một nhãn “hợp lệ/không hợp lệ”.

| Tình huống | Hành động hệ thống đề xuất ở mức an toàn | Quy tắc còn cần chốt |
|---|---|---|
| Mã không có, trùng mã, ảnh tham chiếu lỗi | Dừng tra/xác minh và chuyển người phụ trách | Ai sửa nguồn dữ liệu, có cho tiếp tục bằng quy trình khác không |
| Không có mặt, ảnh kém, nhiều mặt trong vùng | Hướng dẫn thử lại; hết số lần/giới hạn thì chuyển người phụ trách | Số lần thử, timeout và cách chọn vùng làm thủ tục |
| Bằng chứng 1:1 không khớp hoặc không chắc | Chuyển kiểm tra thủ công, giữ điểm và lý do; không tự kết luận mất quyền dự thi | Ngưỡng, tài liệu kiểm tra bổ sung, người quyết định |
| Khớp mặt nhưng sai phòng/ca/môn | Báo đúng loại xung đột và chuyển người phụ trách | Có hướng dẫn chuyển phòng hay quy trình thay đổi phân phòng không |
| Đến ngoài khoảng giờ, lượt đã ghi trước | Không tự ghi lượt thường lệ lần nữa; chuyển xử lý | Mốc “muộn”, quyền chấp nhận, quy tắc sửa/hủy trùng |
| Không có lượt hợp lệ khi tới mốc đối soát | Hiển thị “chưa có lượt ghi nhận” để đối soát | Khi nào mới được gọi là “chưa đến/vắng” và ai xác nhận |

Đây là **hành động đề xuất để không che lỗi**, chưa phải quy định của bất kỳ kỳ thi nào. Một lượt được tự ghi nhận chỉ khi tất cả điều kiện nghiệp vụ đã được phê duyệt và bằng chứng kỹ thuật đạt mức chấp nhận; mức tự động hóa cụ thể còn mở.

## 6. Rủi ro và cách suy tiêu chí đo

- **Chấp nhận nhầm người:** có thể ghi nhận sai danh tính và làm sai đối soát. T-010 phải đo false match tại một operating point được chọn trên development set; kết quả test không được dùng để sửa ngưỡng sau đó.
- **Từ chối nhầm người hợp lệ:** gây chậm, ùn hàng hoặc phải can thiệp thủ công. Vì vậy cần đo false non-match, tỷ lệ retry/manual và thời gian từng lượt, đồng thời giữ đường xử lý con người.
- **Sai người mục tiêu, sai danh sách hoặc sai rule:** có thể tạo lỗi đầu-cuối dù face verification riêng tốt. Cần kịch bản và nhãn theo từng stage; accuracy một model không đại diện toàn hệ thống.
- **Mục tiêu giảm nhân sự:** cần pilot với quy trình và quy chế thật, số lượt/giờ, số người bố trí, thời gian xử lý và khối lượng ngoại lệ. Baseline trên dữ liệu công khai chỉ chứng minh hiệu năng kỹ thuật trong điều kiện đo đã ghi.

Chưa đặt ngưỡng số cho FMR/FNMR, latency, retry, số lần thử, RAM hay thời gian phục vụ vì chưa có kỳ thi, thiết bị và mức rủi ro được chốt. T-010 phải ghi tiêu chí chấp nhận **trước** khi xem kết quả test.

## 7. Cấu hình nghiệp vụ để cùng nhóm lựa chọn

Quốc An xác nhận ngày 2026-09-25 rằng nhóm **chưa chốt kỳ thi cụ thể** và muốn cùng xây bộ nghiệp vụ trước. Vì vậy, prototype cần mô tả một **phiên thi giả lập có phòng, ca, danh sách và ảnh tham chiếu**, rồi tách chính sách từng kỳ thi thành cấu hình được người tổ chức phê duyệt. Không dùng một mốc giờ hoặc quyền xử lý tự nghĩ ra như thể áp dụng cho mọi kỳ thi.

| Nhóm chính sách | Phương án nghiên cứu/đề xuất | Điều cần chốt trước khi vận hành thật |
|---|---|---|
| Mức tự động hóa | Thiết bị xử lý và ghi vết lượt thường lệ; ca ngoại lệ sang người phụ trách. Có thể chạy chế độ chỉ hỗ trợ đối chiếu nếu quy chế yêu cầu con người quyết định. | Kỳ thi nào cho phép tự ghi nhận và bước nào bắt buộc giám thị thực hiện |
| Mốc thời gian | Cấu hình giờ mở lượt, mốc bắt đầu thi, mốc xem là muộn và mốc đối soát vắng; mọi mốc có nguồn. | Giá trị và hệ quả của từng mốc theo quy chế/ban tổ chức |
| Lượt trùng và sửa sai | Không tự tạo hai lượt hợp lệ cho cùng người + ca; mọi sửa đổi có người, lý do, thời điểm và trạng thái trước/sau. | Ai được hủy/ghi đè, có cần duyệt hai cấp hay biên bản không |
| Sai phòng/ca | Hiển thị phòng/ca theo roster và chuyển người phụ trách; không tự đổi phân phòng. | Có cho hướng dẫn sang phòng khác; ai được thay roster |
| Không khớp hoặc ảnh kém | Có retry trong giới hạn; sau đó chuyển thủ công, lưu lý do kỹ thuật và nghiệp vụ riêng. | Số lần thử, bằng chứng bổ sung và người ra quyết định |
| “Chưa đến” | Chỉ là trạng thái báo cáo sau mốc đối soát; không dùng để suy người đó không có quyền thi. | Mốc chốt danh sách vắng và nguồn xác nhận cuối |

**Hai chế độ sản phẩm cần so sánh:** (A) thiết bị đưa kết quả và giám thị xác nhận mọi lượt; (B) thiết bị tự ghi nhận lượt thường lệ theo chính sách được duyệt, giám thị xử lý ngoại lệ. D-001 đặt **B là mục tiêu nghiên cứu** để giảm công đối chiếu lặp lại, nhưng với kỳ thi có quy định người phải đối chiếu trực tiếp thì chỉ được trình bày A như hỗ trợ, không tuyên bố B được áp dụng. Hiệu quả giảm nhân sự của B vẫn cần pilot.

**Tham chiếu để kiểm tra ranh giới, không phải quy tắc mặc định:** [Quy chế thi tốt nghiệp THPT ban hành cùng Thông tư 24/2024/TT-BGDĐT](https://vqa.moet.gov.vn/uploads/news/2024_12/final-quy-che-thi-tot-nghiep-thpt.pdf), mục trách nhiệm thí sinh và nhiệm vụ giám thị, có yêu cầu con người đối chiếu danh sách ảnh/giấy tờ và quy định riêng về mốc đến chậm, báo vắng. Vì nhóm chưa chọn kỳ thi THPT và văn bản có thể được sửa đổi, T-008 không lấy các mốc hay quyền trong đó áp thẳng cho prototype. Nếu về sau chọn kỳ thi này, cần kiểm tra bản có hiệu lực tại thời điểm áp dụng và ghi nguồn trong quyết định.

## 8. Câu hỏi cần nhóm/đơn vị tổ chức trả lời

1. Kỳ thi mục tiêu và quy chế nào là nguồn chuẩn? Bước nào thiết bị được hỗ trợ hoặc tự ghi nhận, bước nào giám thị vẫn phải làm?
2. Quy trình hiện tại có số đo về số người tại cửa, thời gian/lượt, tắc hàng và lỗi để so với pilot không?
3. Ai chốt danh sách/ảnh và phiên bản dữ liệu; ai có quyền sửa dữ liệu hoặc ghi nhận ngoại lệ?
4. Mốc giờ và quyền xử lý đến muộn, nhầm phòng/ca, trùng lượt, rút lui hoặc chưa đến là gì?
5. Thiết bị chạy trong điều kiện camera/ánh sáng/kết nối nào; tối thiểu cần chạy offline hay có thể dùng backend?
6. Dữ liệu ảnh tham chiếu được lấy, lưu, truy cập và xóa theo quy trình nào; demo chỉ dùng dữ liệu công khai/giả lập ở phần nào?

Các câu hỏi này được theo dõi chung tại [questions.md](../00-project/questions.md). Khi có câu trả lời từ thầy hoặc đơn vị tổ chức, cần biên bản nguồn trước khi đổi thành quyết định/chính sách.

## 9. Điều kiện bàn giao sang T-009/T-010

T-008 tạo bản đồ yêu cầu BR-01–BR-08 và các giả định còn mở. **T-009** dùng BR-02–BR-04 để kiểm tra candidate dữ liệu/weight; **T-010** dùng BR-01, BR-05–BR-08 và rủi ro ở mục 6 để khóa fixture, protocol và tiêu chí chấp nhận. Chỉ xem T-008 hoàn tất sau khi nhóm review quy trình, quyền xử lý và trạng thái; những điểm chưa có nguồn vẫn được ghi là câu hỏi, không tự điền bằng suy đoán.
