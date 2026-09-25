# T-005 / Quốc An — Khảo sát dataset theo technical task

**Trạng thái:** candidate survey từ [phân rã S0–S11](quoc-an-task-decomposition.md), chưa tải/kiểm tra toàn bộ tệp, chưa có final dataset. Không có một “dataset của cả hệ thống”. Các số lượng dưới đây là số **nguồn gốc công bố**, chưa phải số mẫu hợp lệ sau lọc. Không commit ảnh mặt hoặc nhãn danh tính.

## 1. Dataset requirements trước khi nêu tên tập

| Task/stage | Dữ liệu và annotation tối thiểu | Vai trò dữ liệu cần phân biệt | Điều dataset không thể chứng minh |
|---|---|---|---|
| S3 phát hiện mặt | ảnh **nguyên khung**, bbox mọi mặt, điều kiện mặt nhỏ/che/góc, split công bố; nếu model trả landmark thì cần nhãn landmark tương thích | Train/fine-tune chỉ nếu huấn luyện detector; development cho confidence/NMS; test và external test | Bbox không cung cấp identity, không đo xác minh 1:1 |
| S4 chọn người đang làm thủ tục | frame/video có nhiều người, nhãn **người mục tiêu của một giao dịch**, track ID, vùng đứng, thời điểm bắt đầu/kết thúc | Development để thiết kế luật chọn; test theo cảnh/camera khác | Nhiều bbox đơn thuần không xác định ai đã khai báo mã |
| S5 chất lượng và S6 căn chỉnh | nhãn mờ/sáng/pose/che nếu đánh giá quality trực tiếp; landmark chuẩn nếu đánh giá alignment; quan trọng hơn là identity và kết quả verification trước/sau chọn ảnh | Component test; development của chính sách quality; external test dưới điều kiện xấu | Điểm “ảnh rõ” không tự chứng minh giảm false match |
| S7 encoder nếu train/fine-tune | nhiều identity, nhiều ảnh/identity, nguồn/điều khoản rõ, split identity-disjoint với test; đủ độ đa dạng và compute | Train/validation riêng; không lấy người của benchmark làm lớp train rồi báo test trên họ | Một tập vài chục người không đủ chứng minh encoder tổng quát |
| S8 verification 1:1 | identity, ảnh reference và probe khác lần thu; genuine/impostor claims hoặc protocol cặp; cần cả người không khớp | Development/threshold calibration, main test, external stress test tách bạch | Tập ảnh đã crop không đo lỗi detection, target selection hay latency camera |
| S2/S4/S5/S8 video qua cửa | sequence gốc, timestamp/frame order, identity, ảnh tham chiếu tách khỏi probe, variation vị trí/ánh sáng; lý tưởng có người nền gắn nhãn | End-to-end vision test và latency proxy | Video một người không đo chọn đúng người giữa nhiều mặt |
| S9–S10 nghiệp vụ | roster, room/session/time/eligibility/check-in state giả lập và expected transition | Software test fixture | Không là face dataset; pass business test không chứng minh nhận diện |
| S11 PAD tùy chọn | bona fide và nhiều loại trình ảnh/video trên thiết bị thu, nhãn tấn công | Chỉ đánh giá riêng nếu tích hợp | PAD accuracy không thay FMR/FNMR xác minh |

**Giao thức quyền dùng:** xem giấy phép của *ảnh*, annotation, code và pretrained weights riêng. Dùng cho đồ án phi thương mại không đồng nghĩa tự được dùng để xây sản phẩm bán; không đưa ảnh/embedding nhạy cảm lên Git. Đánh giá trên ảnh người nổi tiếng hoặc quần thể nhỏ cũng không xác nhận hiệu quả trên thí sinh Việt Nam.

## 2. S3 — candidate cho face detection

**Không gian ứng viên từ yêu cầu:** cần ảnh nguyên khung và bbox; khu vực hành lang có thể nhiều mặt, mặt nhỏ/che. Tìm benchmark có nhiều mặt và một benchmark ngoại lai. Nếu không huấn luyện detector, không cần tạo “train split” mới chỉ để chạy pretrained model.

- **[WIDER FACE](https://shuoyang1213.me/WIDERFACE/):** bài báo gốc ghi **32.203 ảnh, 393.703 bbox khuôn mặt**, 60 nhóm sự kiện, train/validation/test; annotation gồm bbox và thuộc tính như occlusion/pose. **Vai trò có thể:** validation để đo AP/recall theo easy–medium–hard và chỉnh threshold nếu không đụng tập test; test chính thức theo protocol; chỉ dùng train nếu fine-tune. **Ưu:** nhiều mặt, quy mô và protocol chuẩn. **Nhược:** ảnh sự kiện web khác camera cửa phòng, bbox gốc không phải nhãn danh tính hay 5 landmarks. Không tự coi 5 điểm từ một bản phát hành của bên thứ ba là annotation gốc. Trang dataset công bố giấy phép CC BY-NC-ND; cần đọc đúng điều khoản trước khi dùng/biến đổi/phát hành ảnh.
- **[FDDB](https://people.cs.umass.edu/~elm/papers/fddb.pdf):** **2.845 ảnh, 5.171 mặt**, annotation vùng mặt dạng **ellipse** và 10-fold protocol; có che, mờ, độ phân giải thấp. **Vai trò có thể:** external detection test. **Ưu:** nguồn/protocol độc lập; **nhược:** cũ và ellipse không so IoU box trực tiếp nếu chưa thống nhất cách chuyển/metric. Không train detector bằng FDDB rồi gọi nó external test. Điều khoản ảnh cần kiểm tra ở nguồn tải.
- **ChokePoint raw frames:** nguồn video lối đi ở mục 5, có face annotations/ground truth cần xác nhận từng file. **Vai trò:** external domain check của detector sau benchmark ảnh chung. **Nhược:** phần lớn một người/frame, quy mô người nhỏ; không thay WIDER FACE cho độ phủ mặt đông.

**Shortlist khảo sát:** WIDER FACE cho detector benchmark; FDDB hoặc khung nguyên bản của tập lối đi để kiểm tra chuyển miền nếu annotation tương thích. Quyết định cuối về train/test phụ thuộc kiểm tra tệp và việc có train lại detector hay không.

## 3. S6 — dataset landmark/alignment chỉ khi cần đánh giá riêng

Nếu detector đã xuất 5 điểm và nhận diện đầu-cuối tốt, phép biến đổi hình học là deterministic; **không tự thêm một model landmark**. Khi lỗi alignment nổi bật, mới cần nhãn chuẩn:

- **[WFLW](https://wywu.github.io/projects/LAB/WFLW.html):** **10.000 mặt** (7.500 train, 2.500 test), **98 landmarks** và thuộc tính pose, expression, illumination, makeup, occlusion, blur theo công bố của tác giả. Ưu: phép thử khó và breakdown; nhược: layout 98 điểm khác 5 điểm của nhiều encoder, cần map 5 điểm tương ứng trước khi tính NME/ảnh align. Quyền ảnh cần xác minh.
- **[300-W](https://ibug.doc.ic.ac.uk/resources/300-W/):** landmark **68 điểm**, challenge test **600 ảnh** (300 indoor, 300 outdoor), dữ liệu dùng cho nghiên cứu. Ưu: benchmark chuẩn; nhược: khác layout 5 điểm và không đại diện chuỗi cửa. Chọn **một** chuẩn landmark tương ứng với nhánh phương pháp, không cộng 68 và 98 điểm như cùng nhãn.

**Shortlist có điều kiện:** chưa cần dataset landmark riêng cho baseline. Chỉ mở WFLW/300-W sau khi lỗi S6 được chứng minh và chọn rõ mapping/metric.

## 4. S7 — dữ liệu training encoder là nhánh có điều kiện

Đồ án có thể benchmark **trọng số pretrained** trước; khi đó dữ liệu huấn luyện gốc thuộc provenance của từng trọng số, nhóm không cần nhận một tập train mới. Nếu thầy xác nhận phải train/fine-tune, candidate space cần xem lại:

- **[DigiFace-1M](https://github.com/microsoft/DigiFace1M):** nguồn Microsoft mô tả 720.000 ảnh/10.000 danh tính cộng 500.000 ảnh/100.000 danh tính, nhãn identity; ảnh tổng hợp, [giấy phép research non-commercial](https://github.com/microsoft/DigiFace1M/blob/main/LICENSE). Ưu: có nguồn/điều khoản rõ; nhược: chênh miền synthetic → real, dung lượng và compute huấn luyện lớn. Vai trò chỉ là **train/fine-tune**, không dùng làm main real-world test.
- **[VGGFace2](https://github.com/ox-vgg/vgg_face2):** bài công bố ghi khoảng 3,31 triệu ảnh/9.131 người với pose/age đa dạng. Tuy nhiên đường cấp phát ảnh gốc cần kiểm tra hiện còn truy cập và quyền dùng; **không đưa vào kế hoạch phụ thuộc** trước khi xác minh.
- **[MS1MV3/Glint360K](https://github.com/deepinsight/insightface/blob/master/recognition/arcface_torch/README.md):** nguồn tác giả ghi khoảng 5,2 triệu ảnh/93 nghìn identity và 17,1 triệu ảnh/360 nghìn identity. Nhãn phù hợp train encoder nhưng quá lớn cho giả định đồ án hiện tại; nguồn và quyền dùng ảnh phải rà riêng với giấy phép code/model. Không shortlist mặc định.

**Kết luận tạm:** không gán training dataset khi chưa quyết định có train/fine-tune và chưa biết compute. Tuyệt đối không fine-tune trên test identity của tập đánh giá rồi báo kết quả tổng quát.

## 5. S8 — candidate cho xác minh 1:1 và ngoại suy

**Nhu cầu:** cặp cùng/khác người, ảnh tham chiếu khác điều kiện với probe, threshold calibration tách test. Tìm ba miền: ảnh tĩnh chuẩn, ảnh khó về chất lượng, video/camera cửa. Số cặp lớn không tương đương số **người độc lập** lớn.

- **[LFW](https://vis-www.cs.umass.edu/lfw/):** 13.233 ảnh/5.749 người theo nguồn tác giả; protocol cặp 6.000 pair. **Vai trò:** smoke/sanity và đối chiếu literature, **không là main test** do bão hòa và không có video cửa. Annotation identity + pair, không phải bbox toàn cảnh. Điều khoản ảnh cần kiểm tra riêng.
- **[XQLFW](https://martlgap.github.io/xqlfw/):** trang tác giả công bố **6.000 cặp** (3.000 genuine/3.000 impostor), 7.263 ảnh/3.743 identity, tập trung chênh chất lượng và độ phân giải. **Vai trò có thể:** external stress test của encoder/verification. Ưu: gần sự chênh giữa ảnh hồ sơ và ảnh camera; nhược: ảnh cặp, không phải video/lối đi và có ảnh suy giảm tổng hợp. Giấy phép mã đánh giá không tự cấp quyền dùng ảnh; kiểm tra gói tải trước.
- **[YouTube Faces](https://www.cs.tau.ac.il/~wolf/ytfaces/):** **3.425 video/1.595 người**, 5.000 cặp video cùng/khác người, protocol 10 split không trùng người giữa split theo trang tác giả. **Vai trò có thể:** external test cho ghép nhiều frame/embedding; ưu nhiều người và variation video; nhược crop/person-centric, bối cảnh phỏng vấn/YouTube khác camera cửa, không đo detection hay target selection từ full frame. Điều kiện tái phân phối ảnh/video cần kiểm tra.
- **[ChokePoint](https://arma.sourceforge.net/chokepoint/):** camera cố định trên cổng, **48 video sequence, 64.204 ảnh mặt**, 25 người ở cổng 1 và 29 ở cổng 2; có raw frames, cropped faces, ground truth và protocol G1/G2. [Giấy phép nguồn](https://arma.sourceforge.net/chokepoint/) cho nghiên cứu phi thương mại và yêu cầu ghi nguồn. **Vai trò có thể:** external end-to-end vision test theo không gian lối đi và thử reference–probe/video; ưu gần camera cửa hơn ảnh web; nhược người ít, khoảng 12 GB, phần lớn khung chỉ một người; hai sequence đông có che khuất chưa cung cấp sẵn claim/nhãn target cho mọi kịch bản. Phải kiểm tra mapping still/reference và protocol trước khi chọn main test. Không khẳng định đã đo S4 nhiều người chỉ vì có tên “crowded”.
- **[SCface](https://www.scface.org/):** **4.160 ảnh/130 người**, có ảnh mugshot và nhiều camera/khoảng cách, protocol verification identity-disjoint; gần ý ảnh đăng ký vs camera kém. Tuy nhiên tác giả yêu cầu công văn cơ quan và giấy thỏa thuận do nhân viên toàn thời gian ký; **loại khỏi shortlist triển khai ngay**, vì đồ án không dựa vào xin quyền truy cập riêng.
- **[IJB-C](https://www.nist.gov/itl/tted/btg/ijb-c-dataset-request-form):** kiểm tra khả năng truy cập cho thấy NIST ngừng phân phối năm 2023; **loại khỏi kế hoạch phụ thuộc**, dù là benchmark khó.

**Shortlist để kiểm tra khả năng dùng, chưa chọn final:** LFW chỉ smoke, XQLFW cho stress chất lượng, YouTube Faces cho video/cặp, ChokePoint cho lối đi. Sau khi tải mẫu và kiểm tra nhãn/quyền, chọn **một main verification protocol** cộng 1–2 external tests; không lấy trung bình accuracy của chúng thành một điểm “tốt nhất”.

## 6. S4 — khoảng trống dữ liệu người mục tiêu giữa nhiều mặt

WIDER FACE có nhiều bbox nhưng không biết người nào vừa khai báo Candidate ID. ChokePoint có video lối đi nhưng đa số một người/frame. YouTube Faces chủ yếu video đã crop theo một người. **Chưa tìm được trong shortlist công khai một tập vừa có nhiều mặt quanh cửa, vừa có claim/reference và nhãn target theo từng giao dịch.** Vì vậy:

1. Giai đoạn đầu dùng chính sách chọn mặt bảo thủ: chỉ xử lý khi đúng một mặt trong vùng đứng/track ổn định; còn lại retry/manual.
2. Kiểm thử logic với kịch bản bbox/track **giả lập** và có thể đánh giá detector nhiều mặt trên WIDER FACE.
3. Không viết “hệ thống đã chứng minh chọn đúng thí sinh giữa hành lang đông” nếu không có nhãn giao dịch tương ứng.
4. Nếu sau này tìm được tập công khai phù hợp, ghi phiên bản, protocol và bổ sung external test; không thay âm thầm tập test đã khóa.

## 7. Mapping stage → dataset → role và giới hạn

- **S3 detection:** WIDER FACE validation/test (component); FDDB hoặc raw portal frames (external).
- **S4 target selection:** chưa có benchmark giao dịch công khai đủ nhãn; synthetic rule fixtures chỉ kiểm tra logic, không chứng minh thị giác thực địa.
- **S5 quality / S6 alignment:** WFLW/300-W chỉ khi nghiên cứu landmark; XQLFW đo ảnh khác chất lượng qua verification, không phải ground truth “chất lượng tốt”.
- **S7 encoder training:** chưa gán dữ liệu; DigiFace-1M là candidate có điều kiện nếu train/fine-tune trở thành yêu cầu.
- **S8 verification:** LFW smoke; XQLFW, YouTube Faces và ChokePoint là shortlist theo ba mục tiêu stress khác nhau. Chưa có final main set.
- **S9–S10 nghiệp vụ:** fixtures giả lập theo bảng trạng thái và expected outcome.
- **S11 PAD:** không khảo sát dataset ở T-005 core; nếu thêm mô-đun này, mở protocol/dataset riêng.

## 8. Phép biến đổi, leakage và quyết định còn thiếu

Không trộn frame cùng lượt giữa development/test; không dùng ảnh probe của test làm ảnh tham chiếu hoặc để chọn ngưỡng. Với cặp được sinh thêm, cố định seed, số attempt và hạn chế một identity thống trị; báo số người, cặp và phiên riêng. Protocol tác giả được ưu tiên; nếu tạo protocol reference–probe mới, công bố manifest và lý do. Một dataset có thể phục vụ nhiều task **nếu có annotation tương ứng**, nhưng các tập dùng để chọn tham số không được đồng thời gọi là external unseen test. Cần kiểm tra khả năng overlap giữa identity của tập đánh giá và dữ liệu train của pretrained weights; nếu không chứng minh được không overlap, ghi giới hạn.

Trước khi chốt shortlist thực nghiệm phải xác nhận: file tải đúng, nhãn/ảnh khớp, license của ảnh và annotation, kích thước lưu trữ, số attempt genuine/impostor hợp lệ, cấu trúc reference/probe và protocol có thể tái lập. Các mục trên hiện là **việc phải làm**, không phải dữ liệu đã được tải/kiểm chứng.
