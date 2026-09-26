# T-005 / Quốc An — Thiết kế benchmark, phân tích lỗi và quyết định tối ưu

**Trạng thái:** kế hoạch thực nghiệm, chưa có kết quả đo, baseline thực chạy, bottleneck hay phương pháp tối ưu đã chọn. Đọc sau [phân rã bài toán](T-005-quoc-an-task-decomposition.md), [khảo sát dữ liệu](T-005-quoc-an-datasets.md) và [khảo sát phương pháp/model](T-005-quoc-an-models.md). Các mốc bên dưới là **cổng quyết định**, không phải kết luận thực nghiệm.

## 1. Hai luồng cần tách

- **Runtime tại cửa:** claim mã → truy hồ sơ/ảnh → thu hình → xác định mặt mục tiêu và ảnh đủ chất lượng → căn chỉnh → embedding → so khớp 1:1 → quyết định/retry/manual → kiểm tra phòng, ca, giờ, điều kiện và lượt trước → ghi nhận giao dịch. PAD, nếu tích hợp, là một cổng độc lập với phép so danh tính.
- **Research:** khóa requirements và protocol → xác minh dataset/weight có thể dùng → chạy thử component → shortlist → benchmark baseline trên cùng điều kiện → phân tích lỗi theo stage → chọn bottleneck và mục tiêu tối ưu → triển khai một thay đổi → ablation → đánh giá tập test khóa và tài nguyên thiết bị → kết luận có giới hạn.

Dữ liệu ảnh công khai không chứa đầy đủ roster, claim, giám thị và diễn biến tại cửa phòng thi. Vì vậy báo cáo sẽ tách **chứng cứ component**, **kiểm thử logic giao dịch** và **chứng cứ end-to-end thực địa**. Chưa có loại thứ ba ở hiện tại; không cộng các loại kết quả thành một “accuracy hệ thống”.

## 2. Chuẩn bị giao thức trước khi chạy

### 2.1 Kiểm tra nguồn và manifest

Với mỗi dataset/weight được dùng, ghi nguồn, phiên bản, giấy phép của ảnh/annotation/mã/weight, ngày truy cập, số file tải thực, hash/manifest, số người và số attempt hợp lệ sau lọc. Nếu không truy cập được dữ liệu, thiếu nhãn cần thiết hoặc quyền dùng không rõ, loại khỏi benchmark và ghi lý do; không lặng lẽ thay bằng tập khác. Không đưa ảnh mặt, định danh cá nhân, embedding hoặc checkpoint vào Git.

Mỗi pretrained model phải có ID gồm architecture, tên weight, tập train được nhà phát hành công bố, input size, chuẩn màu, normalization, align template, output dimensionality, runtime và phiên bản/hash. Không coi các trọng số có chung tên kiến trúc là một model. Ghi detector, NMS/confidence, quy tắc chọn mặt và chất lượng, similarity, threshold, chính sách retry, phiên bản mã và seed trong cùng manifest cấu hình.

### 2.2 Tách development, test và external test

- **Train/fine-tune:** chỉ khi thật sự huấn luyện stage S3/S7/S11; không gọi tập phát triển thành tập train vì đã thử nhiều cấu hình trên đó.
- **Development:** chọn cấu hình, threshold, quality rule và vùng uncertain. Mọi lần sửa dựa vào kết quả ở đây đều là tuning.
- **Locked test:** dùng một lần cho báo cáo chính sau khi cấu hình đóng băng; nếu cần sửa sau khi xem test, ghi rõ đây là vòng nghiên cứu mới và có test khác.
- **External/stress:** đánh giá chuyển miền, ảnh kém, video hoặc portal nếu dữ liệu hợp lệ; không dùng để sửa rồi vẫn gọi external unseen.
- **Software fixtures:** hồ sơ và trạng thái check-in giả lập, tách khỏi ảnh benchmark.

Ưu tiên protocol chính thức của dataset. Nếu tự tạo cặp reference–probe, tách theo **identity** giữa development và test; frame/crop cùng video, cùng lần chụp hoặc cùng người không được rơi cả hai phía. Trong mỗi cặp genuine, ảnh tham chiếu và probe phải từ lần thu khác khi metadata cho phép. Impostor có claim mã của người A nhưng probe của B; ghi quy tắc chọn impostor, tỷ lệ và seed. Không đưa ảnh test vào gallery tham chiếu của development hoặc dùng test để tìm threshold. Kiểm tra overlap giữa benchmark identity và tập train của pretrained weights; nếu không xác minh được, báo giới hạn.

### 2.3 So sánh công bằng

So các candidate **cùng task, cùng mức trừu tượng**. Một detector so với detector bằng cùng ảnh nguyên khung và quy tắc đo; encoder so với encoder trên cùng cặp/face crop, nhưng preprocessing chính thức của từng encoder phải giữ và công bố. Khi so một thay đổi pipeline, giữ các component khác, split, camera input, timeout và chính sách quyết định cố định. Báo cả kết quả component và tác động toàn pipeline để tránh tối ưu AP mà không cải thiện xác minh.

Đo latency sau warm-up và bao gồm tiền xử lý/hậu xử lý theo từng stage; đo end-to-end từ khi ảnh sẵn có và, nếu có thiết bị thật, thêm thời gian acquisition/UI riêng. Cùng thiết bị, chế độ nguồn, số luồng, runtime và batch size 1; phân biệt đo PC proxy với đo smartphone/edge thật. Chưa có thiết bị đích nên chưa tuyên bố đạt giới hạn mobile. Ghi median và tail latency (ví dụ p95), peak RAM, dung lượng toàn bộ artifact và throughput nếu phù hợp. FLOPs/parameters chỉ là proxy, không thay latency đo.

## 3. Metric và operating point theo task

| Task/đối tượng | Metric chính cần xem | Metric phụ và phép đọc đúng |
|---|---|---|
| S3 detection | AP/mAP theo protocol của tập; recall theo face size/occlusion và ở confidence được chọn trên dev | false detections/frame, tỷ lệ không thấy mặt mục tiêu nếu có nhãn target; landmark NME chỉ nếu có nhãn đúng schema. WIDER FACE AP không đo danh tính |
| S4 target selection | tỷ lệ chọn đúng target **trên giao dịch có nhãn**, tỷ lệ từ chối mơ hồ | chọn nhầm người nền, timeout, số frame chờ; nếu thiếu nhãn target chỉ báo test logic giả lập và không công bố tỷ lệ thị giác |
| S5/S6 quality + alignment | coverage ảnh được nhận tại mức lỗi xác minh cố định; landmark NME khi dùng benchmark landmark | FNMR/FMR trước/sau quality/align trên cùng cặp, retry rate, latency; ảnh đẹp hay NME thấp chưa đủ |
| S7 Feature extraction / S8a Verification 1:1 / S8b Decision policy | **FNMR tại FMR mục tiêu** do yêu cầu nghiệp vụ/khả năng sample xác định; báo FMR quan sát với khoảng tin cậy | ROC/DET, EER và AUC để mô tả, không dùng EER làm threshold nghiệp vụ mặc định; genuine/impostor score distribution; manual/retry rate và coverage nếu có vùng uncertain |
| S11 PAD nếu thêm | APCER/BPCER hoặc ACER theo protocol PAD; attack-type breakdown | latency và tỷ lệ bona fide bị chặn; không lấy PAD accuracy thay verification |
| S9/S10 quy tắc | test case pass/fail theo bảng trạng thái, tính idempotent/atomic của ghi nhận | trường hợp sai phòng, sai ca, trễ, không đủ điều kiện, mã lạ, lượt trùng, hai request đồng thời, retry và override có audit |
| Runtime/tài nguyên | end-to-end latency tại batch 1 và peak RAM trên thiết bị cụ thể | thời gian từng stage, model bytes, bộ nhớ storage, năng lượng/nhiệt nếu đo được; báo cả thời gian khi retry |
| Giao dịch tổng hợp | tỷ lệ quyết định đúng/nhầm/chuyển tay **chỉ trên tập có đầy đủ claim, target và expected outcome** | thời gian đến kết quả, tỷ lệ manual; không suy ra giảm nhân lực từ benchmark ảnh công khai |

**FMR** là tỷ lệ impostor claim được chấp nhận; **FNMR** là tỷ lệ genuine claim bị từ chối. Với hệ thống cho vào phòng thi, false accept và false reject có hậu quả khác nhau: cần chọn mức FMR mục tiêu theo yêu cầu nghiệp vụ, rồi đo FNMR và tải retry/manual. T-005 chưa tự đặt một con số FMR vì chưa có quy chế/ngưỡng được chốt và số impostor attempts của public data có thể không đủ để ước lượng FMR rất thấp. Báo khoảng tin cậy, denominator, số identity và cặp; khi số liệu không hỗ trợ operating point thì ghi “không ước lượng được đáng tin”, không nội suy thành đảm bảo an ninh.

## 4. Baseline plan: chạy rồi mới kết luận yếu ở đâu

### 4.1 Baseline tối thiểu có thể tái lập

1. **Nghiệp vụ:** mã tra một hồ sơ; hồ sơ thử giả lập; quy tắc phòng/ca/giờ/eligibility/duplicate; transaction log có trạng thái retry/manual. Chạy test độc lập CV.
2. **Vision component:** một detector có bbox + landmark hợp lệ, quality rule tối thiểu, một pretrained face encoder có provenance rõ, similarity theo khuyến nghị của encoder, một threshold học trên dev. Danh tính thí sinh trong test không nằm trong train/tuning. Đây chỉ là cấu trúc baseline; tên weight/threshold được chọn sau bước kiểm tra khả dụng và benchmark candidate.
3. **Video/portal nếu khả thi:** target policy bảo thủ “một mặt trong vùng đứng, ổn định qua cửa sổ frame; còn lại retry/manual”; không tự nhận đây là giải pháp đông người đã được chứng minh.
4. **Đối chứng mạnh:** giữ một pipeline có performance cao nhưng có thể nặng làm mốc tham chiếu nếu trọng số và quyền phù hợp. Nếu về sau tối ưu pipeline nhẹ, báo kết quả với **chính pipeline nhẹ gốc** và mốc mạnh này để trả lời vì sao không dùng model mạnh ngay.

Baseline phải được chạy trên protocol đã khóa và thiết bị đo nêu rõ. Tại thời điểm viết **chưa có baseline thực chạy**, nên không có “baseline yếu ở detection/encoder/threshold” hay model thắng.

### 4.2 Trình tự thí nghiệm để tránh tích tổ hợp vô hạn

- **B0 — khả dụng:** smoke test input/output, giấy phép, bộ nhớ, runtime và reproducibility; chỉ loại candidate vì gate đã công bố, không dựa vào test score.
- **B1 — detection:** so detector trên cùng nguyên khung, cùng metric; sau đó kiểm tra 1–2 detector ở điểm đánh đổi khác nhau khi ghép với encoder cố định.
- **B2 — encoder:** dùng cùng cặp reference/probe và cùng detector/crop đầu vào. Báo chuẩn align riêng nếu bắt buộc; nếu khác, so cả trên face crop chuẩn chung khi có thể và ghi ảnh hưởng preprocessing.
- **B3 — policy:** giữ detector+encoder cố định; so one-threshold với retry band hoặc quality rule chỉ trên dev, xác nhận trên locked test. Không tuning threshold bằng test.
- **B4 — end-to-end có điều kiện:** ghép một số tổ hợp có lý do từ B1–B3. Tập nào chỉ có crop thì không đo được detection hay target selection. Tập portal nào thiếu claim/target đầy đủ thì chỉ báo các stage có nhãn.

Không chạy mọi detector × encoder × quality × threshold; mỗi phép ghép phải trả lời một giả thuyết và giữ đối chứng.

## 5. Error analysis và tìm bottleneck

Ghi từng attempt với claim giả danh, nhãn cùng/khác người, nguồn, điều kiện ảnh, detector bbox/score, landmark/crop, target policy, quality gate, similarity, threshold, quyết định retry/manual, thời gian stage và lý do nghiệp vụ. Ẩn định danh thật và không lưu ảnh/embedding trong Git. Với lỗi, đọc lần lượt: ảnh tham chiếu sai/chất lượng kém → camera/đối tượng → detection → chọn target → quality/align → embedding separation → calibration/policy → business state/transaction. Tránh quy mọi false reject cho encoder nếu mặt mục tiêu chưa vào crop.

Phân tầng lỗi theo mặt nhỏ, pose, mờ, sáng, che, loại thiết bị/camera, loại dataset, genuine/impostor, lượng frame. So score distributions và trường hợp sát ngưỡng; kiểm tra liệu stage sau có thể sửa lỗi của stage trước không. Với nguồn ảnh/video có nhãn tương ứng, chạy **oracle replacement** từng stage (ví dụ ground-truth bbox hoặc target) để ước lượng mức lỗi có thể thu hồi; ghi rõ oracle không là pipeline triển khai. Nếu không có nhãn để đặt oracle, không kết luận stage đó là bottleneck.

Gọi một stage là **bottleneck thực nghiệm** khi: (a) lỗi của stage có đủ mẫu/nhãn để đo; (b) nó chiếm phần đáng kể lỗi giao dịch hoặc tài nguyên theo mục tiêu đã chọn; (c) thay stage bằng oracle/candidate tốt hơn cải thiện metric cuối trên dev/test phù hợp; (d) cải thiện đáng giá chi phí latency/RAM/manual rate. Nếu thiếu (a)–(c), giữ là giả thuyết. Với nhiều bottleneck, ưu tiên theo tác động lên lỗi nghiêm trọng ở operating point đã chốt, rồi khả thi triển khai.

## 6. Quyết định hướng tối ưu chỉ sau baseline

Các nhánh dưới đây là **ứng viên điều tra**, không phải phương pháp được chọn:

- Nếu mất mặt hoặc landmark kém: xem confidence/NMS, detector/landmark, crop và vị trí camera; đo AP/recall, NME nếu có nhãn, rồi FMR/FNMR toàn pipeline và latency.
- Nếu ảnh được chấp nhận nhưng ảnh yếu gây false reject: so quality gate, lựa chọn frame hoặc tổng hợp nhiều frame; đo FNMR tại FMR chốt cùng coverage, retry và thời gian chờ.
- Nếu cặp khó vẫn chồng điểm dù crop đúng: kiểm tra encoder/weight/training compatibility; nếu đổi encoder thì đó là **component selection**, chỉ gọi optimization của encoder khi thật sự có phép can thiệp rõ vào cùng model.
- Nếu score tách được nhưng threshold/policy tạo lỗi: hiệu chỉnh threshold trên dev hoặc thiết kế vùng uncertain; đo FMR/FNMR, coverage và tải manual. Threshold tuning trên test không hợp lệ.
- Nếu độ chính xác đủ nhưng chậm/nặng: thử quantization, distillation/compression hoặc encoder/detector nhẹ hơn theo điều kiện phần cứng; đo lại cả độ chính xác, RAM, size và latency thật. Thay model nhẹ hơn là selection; quantization của cùng model là một can thiệp riêng.
- Nếu chọn nhầm người nền: sửa cách giao dịch xác định người đứng tại vị trí camera, vùng đứng, ambiguity rejection; chỉ nghiên cứu learned tracking khi có dữ liệu target labels. Không dùng kết quả WIDER FACE như chứng cứ cho bài toán này.

Sau khi chọn **một bottleneck chính**, ghi giả thuyết có thể bác bỏ, biến can thiệp, baseline gốc, tập dev/test, metric chính và mức tài nguyên chấp nhận. Không chọn trước PSO/GA/Jaya/Bayesian optimization hay tên thuật toán nào chỉ để có “phần cải tiến”. Nếu một thuật toán tối ưu tham số được đề xuất, phải nói tham số nào, objective/constraints nào, dữ liệu tuning nào, ngân sách search và so với grid/random/manual fair baseline; test giữ kín.

## 7. Ablation để quy kết tác động

- **A0:** pipeline gốc đã khóa trên cùng split/hardware.
- **A1:** chỉ thay một thành phần/hướng can thiệp; giữ detector, encoder, preprocessing, pair list, threshold policy khác cố định khi tương thích. Nếu can thiệp buộc recalibrate threshold, báo cả so tại ngưỡng cũ và sau calibrate dev để thấy phần đóng góp của calibration.
- **A2+ nếu có nhiều cải tiến:** chạy mỗi cải tiến đơn lẻ rồi kết hợp, cùng protocol. Báo gain, regression và chi phí cộng thêm; không quy toàn bộ gain của tổ hợp cho một module.
- **Selection đối chứng:** so pipeline đề xuất với pipeline mạnh nhất ở B1–B4 và chính baseline của nó, tránh “tối ưu model yếu rồi chỉ thắng bản gốc”.
- **Tính ổn định:** bootstrap theo identity/session hoặc lặp seed khi thích hợp, báo khoảng tin cậy; không báo chênh rất nhỏ là thắng chắc khi khoảng tin cậy chồng nhau hoặc protocol nhỏ.

Với các tập khác miền, không gom metric thành một điểm trung bình tùy ý. Báo ma trận theo dataset/điều kiện và Pareto accuracy–latency–RAM–manual rate.

## 8. Framework chốt pipeline sau này

Chỉ chọn final pipeline khi có đủ:

1. Quy tắc nghiệp vụ và operating point đã được người phụ trách chốt; nguồn data/weight có quyền dùng cho **phạm vi đồ án**; phiên bản và protocol tái lập.
2. Có benchmark baseline và proposed trên cùng locked test, báo FMR/FNMR tại operating point, lỗi component, độ trễ/RAM/size trên phần cứng nêu rõ.
3. Có error analysis chỉ ra bottleneck, ablation quy kết gain và đối chiếu pipeline mạnh khác. Nếu proposed tăng accuracy nhưng tăng manual/latency quá mức, nêu trade-off thay vì gọi thắng tuyệt đối.
4. Có kiểm thử transaction cho sai phòng/ca/giờ, trùng lượt và lỗi ngoại lệ; phần này là bằng chứng software, không thay benchmark face verification.
5. Tuyên bố đúng giới hạn: thiếu nhãn target giữa hành lang đông, thiếu ảnh đăng ký thí sinh Việt Nam/thiết bị thật, không có phép đo giảm nhân lực và PAD nếu chưa tích hợp. Không gọi bản demo là hệ thống được phép thay giám thị trong kỳ thi thật.

**Quyết định cuối hiện còn mở:** dataset main test, model/weight cụ thể, detector/encoder thắng, thiết bị mục tiêu, ngưỡng và mục tiêu tối ưu. Đây là kết quả khảo sát T-005 để chuẩn bị thực nghiệm, không phải báo cáo kết quả thực nghiệm.
