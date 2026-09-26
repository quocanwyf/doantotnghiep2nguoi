# T-005 / Quốc An — Khảo sát phương pháp và model theo task

**Trạng thái:** survey candidate space sau [phân rã task](T-005-quoc-an-task-decomposition.md) và [yêu cầu dataset](T-005-quoc-an-datasets.md). **Chưa có selected model, selected detector hay final pipeline.** Một architecture, loss, trọng số pretrained và pipeline hoàn chỉnh là bốn cấp khác nhau; không so chúng như bốn “model” ngang hàng.

## 1. Ngôn ngữ so sánh và yêu cầu lọc chung

- **Task:** ví dụ face detection, face embedding, 1:1 verification.
- **Method/family:** ví dụ detector một lượt có landmark; embedding + similarity.
- **Architecture/backbone:** ví dụ lightweight CNN, residual CNN, efficient transformer.
- **Training objective:** triplet hoặc margin-based loss; [ArcFace](https://openaccess.thecvf.com/content_CVPR_2019/papers/Deng_ArcFace_Additive_Angular_Margin_Loss_for_Deep_Face_Recognition_CVPR_2019_paper.pdf) là **loss**, không phải một file trọng số.
- **Pretrained model:** architecture + weight cụ thể + training data + preprocessing + phiên bản/hash + quyền dùng.
- **Pipeline:** detector + target policy + alignment + encoder + similarity + decision policy + nghiệp vụ.

**Hard gate trước benchmark:** có nguồn chính thức/đáng kiểm chứng và trọng số tải được cho nghiên cứu; input/output và preprocessing tài liệu hóa; chạy được trên runtime thử của nhóm; giấy phép học thuật không cấm dùng; đầu ra phù hợp stage. Giới hạn mobile **chưa có con số** nên kích thước, FLOPs, RAM và latency là tiêu chí sàng lọc tương đối, không đặt cutoff giả. **Soft criteria:** evidence ở đúng task, khác biệt kiến trúc có ích, mức duy trì/documentation, khả năng xuất ONNX/TFLite/Core ML hay runtime tương đương, số phép thử tối đa. Benchmark literature chỉ giúp quyết định *đáng thử*, không là kết quả của đồ án.

## 2. S3 detection/localization — candidate space trước shortlist

**Task cần giải:** từ ảnh nguyên khung trả nhiều bbox và, tốt nhất, 5 landmark cho mỗi mặt. Detector người/vật nói chung hoặc face classifier không trực tiếp giải quyết đầu ra này.

**Family 1 — cascade nhiều lượt:** [MTCNN](https://arxiv.org/abs/1604.02878) vừa detect vừa landmark. Có giá trị làm đối chiếu lịch sử, nhưng nhiều lần suy luận làm chi phí runtime tăng; chỉ đưa benchmark nếu implementation/latency thực tế cạnh tranh, không ưu tiên mặc định.

**Family 2 — face-specific single-shot nhẹ:** [MediaPipe Face Detector/BlazeFace](https://developers.google.com/edge/mediapipe/solutions/vision/face_detector) tối ưu mobile và trả bbox/keypoints; [OpenCV YuNet](https://github.com/opencv/opencv_zoo/blob/main/models/face_detection_yunet/README.md) có trọng số ONNX và landmark. Cả hai đáng kiểm tra vì đầu ra ghép được với alignment và có đường chạy thiết bị. Cần kiểm tra cấu hình short/long range của BlazeFace so khoảng cách camera thật; pin phiên bản YuNet vì repo có nhiều file model.

**Family 3 — face-specific detector nhiều mức compute:** [SCRFD](https://github.com/deepinsight/insightface/blob/master/detection/scrfd/README.md) công bố các cấu hình từ nhẹ đến nặng; [RetinaFace](https://arxiv.org/abs/1905.00641) ghép bbox/landmark, có backbone nhẹ và nặng. Chúng giúp thấy accuracy tăng bao nhiêu khi thêm compute. Trọng số InsightFace phát hành cần xem [điều khoản model zoo](https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md) riêng với mã.

**Family 4 — generic object detector hoặc YOLO-face biến thể:** một backbone YOLO gốc chỉ xuất object bbox nếu chưa train đúng face/landmark. Không benchmark tên “YOLO” trừ khi xác định bản face-specific, weight, schema landmark và giấy phép; cùng lý do không lấy EfficientNet/ViT classification đặt vào slot detector mà không có head/weight tương ứng.

**Lọc bước đầu, chưa phải thắng thua:** shortlist tối đa một đại diện mobile-native (MediaPipe), một face-specific ONNX rất gọn (YuNet), một đại diện nhiều mức compute (SCRFD nhẹ). RetinaFace-Mobilenet là phương án thay nếu trọng số/runtime của một đại diện trên không dùng được; MTCNN và YOLO-face chưa vào benchmark gọn vì chưa mang thêm câu hỏi rõ so với ba họ đã có. Số model thực tế giảm tiếp sau kiểm tra trọng số, schema keypoint, license và một lượt chạy thử. Không lấy AP công bố từ repo khác protocol rồi xếp hạng trước khi chạy trên cùng tập/thiết bị.

## 3. S4 target selection và tracking — có cần model riêng?

**Task:** xác định track của người đã khai báo mã, trong khi detector có thể thấy người nền. Một detector chỉ tìm mọi mặt, **không biết ai cầm mã**. Candidate method theo độ phức tạp:

1. Một vùng đứng giao dịch + đúng một bbox/track ổn định trong vùng; nếu mơ hồ thì retry/manual.
2. Liên kết bbox qua frame bằng IoU/khoảng cách tâm/kích thước và timeout; kiểm tra tính liên tục.
3. Tracker học máy hoặc person re-identification riêng chỉ nếu dữ liệu có nhãn target/track và lỗi baseline chứng minh cần.

**Shortlist:** luật không học + ambiguity rejection cho baseline. Chưa shortlist tracker học máy vì [khảo sát dữ liệu](T-005-quoc-an-datasets.md) chưa tìm được benchmark công khai đủ claim + target labels quanh cửa. Không tuyên bố chọn đúng người trong đám đông bằng cách thử detector trên WIDER FACE.

## 4. S5 quality và S6 alignment — tách rule khỏi learned model

**Quality:** trước hết xét kiểm tra xác định: kích thước mặt/eye distance, blur proxy, ánh sáng, pose từ landmark, che khuất thô và số frame chờ tối đa. Candidate learned face-quality model chỉ hợp lý nếu (a) có weight/dataset phù hợp; (b) điểm của nó dự đoán **verification utility**, không chỉ “ảnh đẹp”; (c) vượt quy tắc đơn giản trên test độc lập với chi phí chấp nhận được. Chưa chọn tên model quality nào khi chưa thấy bottleneck.

**Alignment:** nếu S3 xuất 5 điểm, dùng phép biến đổi hình học chuẩn hóa đến template của **encoder cụ thể**, không có neural network mới. Nếu detector không có landmark hoặc điểm sai, candidate gồm detector khác có landmark hoặc landmark regressor độc lập; model 68/98 điểm chỉ có ý nghĩa khi map đúng sang nhu cầu encoder. So metric landmark riêng và ảnh hưởng FNMR/FMR đầu-cuối; landmark NME thấp hơn chưa chắc xác minh tốt hơn.

## 5. S7 representation — họ encoder và candidate pool

**Yêu cầu:** tạo embedding của hai ảnh cùng người gần nhau hơn ảnh khác người, nhưng vẫn dùng được với **danh tính chưa thấy lúc huấn luyện**. Runtime không dự đoán class của từng thí sinh. Một general image classifier backbone chỉ trở thành face encoder khi có đầu ra embedding, face training objective và trọng số tương ứng.

- **Lightweight face-specific CNN:** [MobileFaceNets](https://arxiv.org/abs/1804.07573) là kiến trúc được thiết kế cho xác minh trên thiết bị hạn chế; một weight cụ thể từ [model zoo InsightFace](https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md) có thể đại diện nếu provenance/đầu vào đã kiểm tra. Đây là candidate về **đánh đổi tài nguyên**, không tự nhận tốt nhất. Tên architecture không đủ để chạy.
- **Lightweight transformer/hybrid:** [EdgeFace](https://github.com/otroshi/edgeface) phát hành các biến thể nhỏ và trọng số, kèm báo cáo về edge/compact benchmark. Đáng thử để có một họ khác CNN; cần kiểm tra bước align, export/runtime và quyền trọng số chứ không suy từ [BSD-3-Clause của mã](https://github.com/otroshi/edgeface/blob/main/LICENSE) sang toàn bộ dữ liệu huấn luyện.
- **Residual CNN với chất lượng ảnh:** [AdaFace](https://github.com/mk-minchul/AdaFace) phát hành R18/R50 và dùng quality-adaptive training; R18 là candidate để kiểm tra ảnh kém chất lượng. “AdaFace” chỉ tên phương pháp/loss; phải chỉ rõ weight R18 đã train trên tập nào, input BGR và version.
- **Residual CNN mạnh làm tham chiếu:** một R50 face encoder với trọng số công bố từ [InsightFace model zoo](https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md) là candidate quality ceiling. R100 hoặc ViT lớn hơn chỉ thêm nếu R50 còn khả thi và câu hỏi nghiên cứu cần; nếu vượt ngân sách/không có runtime thiết bị, không đưa vào shortlist mobile.
- **Generic EfficientNet/ResNet/ViT:** đây là backbone family. EfficientNet ImageNet classifier không trực tiếp cho embedding danh tính. Chỉ xét weight đã được **face-trained** và có preprocessing/rights rõ. **FaceNet** mô tả embedding/triplet method, không phải một trọng số có thể so trực tiếp với một pack.

**Shortlist có điều kiện để benchmark tối đa 3–4 encoder khác vai trò:** một MobileFaceNet pretrained hợp lệ, một EdgeFace compact, một AdaFace R18 và một R50 mạnh để làm điểm tham chiếu. Việc có bốn tên ở đây là **kết quả lọc family/khả dụng**, không phải ấn định final four; số lượng còn lại sau kiểm tra weight, quyền, export và test chạy nhỏ có thể ít hơn. Không benchmark hai weight gần như cùng backbone/training chỉ vì tên pack khác. Nếu một weight chứa detector bundled, tách detector và encoder khi muốn quy kết tác động.

## 6. S8a Verification 1:1 và S8b Decision policy

**Giải pháp cơ bản:** cùng encoder và preprocessing tạo e(reference), e(probe); normalize nếu model yêu cầu; tính cosine similarity hoặc khoảng cách công bố; chọn ngưỡng trên **development set**; trả match/non-match/uncertain. Không nhất thiết thêm neural network “verification” thứ ba. Nếu train một binary classifier trên cặp embedding, phải chứng minh hơn ngưỡng đơn giản và có dữ liệu identity-disjoint đủ lớn; hiện không shortlist.

**Candidate policy:** một ngưỡng; hai ngưỡng có vùng retry/manual; hoặc score từ nhiều frame nếu sau này có bằng chứng. Threshold khác model và khác domain, không copy giá trị từ tài liệu. Một vùng uncertain tăng an toàn nhưng làm tăng manual rate; metric phải báo cả hai.

## 7. S9–S10 nghiệp vụ và S11 PAD

Phòng/ca/giờ/eligibility/trùng lượt là so sánh dữ liệu và chuyển trạng thái **deterministic**. Dùng test case và transaction/idempotency, không tìm dataset/model ML. PAD có task bona fide vs presentation attack, cần nguồn dữ liệu/metric riêng nếu được đưa vào phạm vi; ở T-005 core chỉ ghi giao diện/giới hạn. Face similarity cao không xác nhận người trước camera là người sống.

## 8. Từ component đến pipeline ứng viên: tạo sau kiểm tra khả dụng

Không có sẵn “pipeline A/B/C” ngay lúc khảo sát. Sau khi shortlist từng stage được xác nhận, tạo một ma trận **nhỏ có mục đích**:

1. Giữ một encoder cố định, so các detector/landmark bằng detection metric và FNMR/FMR đầu-cuối. Chỉ giữ 1–2 detector trên đường đánh đổi.
2. Giữ một detector/ảnh align cố định, so các encoder ở cùng ảnh/cặp để đo representation. Dùng preprocess đúng của từng encoder; nếu align khác, ghi rõ yếu tố còn thay đổi.
3. Ghép tối đa vài tổ hợp có lý do và đo end-to-end trên raw frame/video. Không chạy tích Descartes của mọi candidate.
4. Giữ pipeline mạnh chưa tối ưu làm đối chứng ngoài; nếu một pipeline nhẹ được chọn để cải thiện, phải so proposed với **chính nó trước cải thiện lẫn pipeline mạnh**.

Tên/phiên bản của pipeline chỉ được đặt khi các component thật sự chạy được và protocol đã khóa. [Thiết kế thí nghiệm](T-005-quoc-an-experiments.md) mô tả metric, split, baseline và cổng quyết định đó.

## 9. Những điều chưa được quyết

Chưa biết model nào thắng; chưa có benchmark trên cùng dữ liệu/phần cứng; chưa pin weight/hash; chưa xác nhận mobile runtime và giới hạn tài nguyên; chưa có bằng chứng stage nào yếu nhất. Do đó mọi shortlist ở đây mang nhãn **candidate to validate**, không phải final model. Lựa chọn training/fine-tune và optimization method chỉ hình thành sau baseline và trao đổi yêu cầu học thuật với thầy.
