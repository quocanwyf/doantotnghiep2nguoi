# T-022 — Audit và khóa benchmark S8 controlled two-face từ XQLFW

**Ngày:** 2026-09-29. **Người thực hiện:** Quốc An cùng Codex. **Trạng thái:** benchmark và nhãn proxy đã khóa trước score; **chưa chạy development cosine/P2, chưa mở evaluation**. T-021 và [chuỗi quyết định](DECISION_LOGIC.md) là đầu vào. Đây là **synthetic/controlled proxy** ghép từ ảnh XQLFW, không phải ảnh cửa phòng thi hay lượt check-in thật.

## Observation → question → protocol → evidence → decision

T-017 còn hai target-absent proxy trial mà P2 chọn non-target. T-020 cho thấy S8 replay dùng lại cùng cosine, nên hai lựa chọn đó vẫn được accept. Câu hỏi tiếp theo là: **trên dữ liệu có identity ground truth rõ, genuine, ordinary impostor và non-target được S4 chọn phân bố score/trade-off ra sao?** T-022 trước hết dựng và khóa dữ liệu, không chọn ngưỡng. Dataset được xác định bằng nhãn nguồn và kiểm ảnh **trước** khi xem cosine hoặc output P2.

## Nguồn và cách dựng cảnh

- Nguồn: XQLFW ZIP và official `pairs.txt`. Folder identity và nhãn pair cùng/khác identity là ground truth nguồn. Script xác nhận 6.000 dòng pair hợp lệ, member tồn tại và nhãn pair nhất quán với folder identity. Độ đúng tuyệt đối của nhãn công khai vẫn là giới hạn nguồn; không có reviewer độc lập.
- Giữ split identity-disjoint T-014, loại identity đã có trong pilot và manifest T-015/T-017. Không dùng hai failure T-017/T-020 để chọn ảnh, nhãn hay tham số.
- Với mỗi anchor identity A, chọn một positive pair nguồn: `A_ref` và `A_scene`. Chọn một ảnh B của identity khác A từ negative pair nguồn; chọn C của identity thứ ba. **Target-present** ghép hai tile `[A_scene, B]`, đáp án là panel A. **Target-absent** ghép `[B, C]`, đáp án `NONE`. Reference cho cả hai là `A_ref`. Thứ tự trái/phải được quyết định bằng seed, không dùng similarity.
- Mỗi tile giữ nguyên ảnh JPEG 250 × 250, không scale; ghép PNG không mất dữ liệu với gutter xám 16 px. Một trial có **hai panel ảnh**, nhưng ảnh nguồn đôi khi còn mặt nền; vì thế phải qua kiểm detector và kiểm trực quan mới được gọi là controlled two-face *usable*.
- Ground truth `target_panel` hoặc `NONE` được ghi trong candidate manifest khi tạo cảnh, **trước detector box và trước recognition score**. Box chỉ nối nhãn panel nguồn với mặt detector tìm được, không tự sinh identity.

## Audit và mẫu số đã khóa

SCRFD của B0 chạy **detection-only**, `det_size=(640,640)`, `det_thresh=0.5`, CPU. Recognition module không được nạp. 5.168 ảnh nguồn được kiểm: 4.446 ảnh có đúng một detection, 505 ảnh nhiều detection, 217 ảnh không có detection. Cảnh chỉ đạt kỹ thuật khi reference và hai tile nguồn đều có đúng một detection, cảnh ghép có đúng hai box và mỗi panel một box. Để giữ hai loại cảnh của cùng anchor tương ứng, nếu một cảnh không đạt detector thì **cả cặp present/absent** loại khỏi tập khóa. Tất cả 20 contact sheet, tổng 160 anchor, được tự kiểm trực quan; 21 anchor được đánh dấu `AMBIGUOUS` qua hai lượt tự rà soát trước score vì người nền/mặt thêm hoặc liên hệ reference–target không đủ chắc. Không dùng output nhận diện để quyết định giữ/loại.

| Nhóm đã khóa | Development | Evaluation | Diễn giải |
|---|---:|---:|---|
| Anchor candidate | 96 | 64 | Mỗi anchor sinh một present và một absent scene |
| Present usable | 32 | 30 | Box–panel và nhãn nguồn nhất quán qua self-confirm |
| Absent usable | 32 | 30 | A vắng theo ba folder identity khác nhau và kiểm ảnh |
| Present/absent `AMBIGUOUS` | 14 / 14 | 7 / 7 | Không ép nhãn, loại khỏi metric khóa |
| Present/absent excluded bởi detector | 50 / 50 | 27 / 27 | Một hoặc cả hai cảnh trong cặp không đạt điều kiện kỹ thuật |
| Genuine pair 1:1 usable | 1.318 | 355 | Official positive pair, hai ảnh nguồn đúng một detection |
| Ordinary-impostor pair 1:1 usable | 992 | 131 | Official negative pair, khác identity, không trùng chính cặp ảnh nguồn dùng trong cảnh khóa |
| Pair nguồn excluded bởi detector | 843 | 113 | Gộp genuine và ordinary negative |
| Ordinary pair excluded do trùng scene pair | 9 | 14 | Tránh cùng cặp ảnh xuất hiện ở nhóm ordinary và cảnh S4 |
| S4-derived hard-negative pair | **Chưa có mẫu số** | **Chưa có mẫu số** | Chỉ xác định sau khi P2 cố định chạy trên 40/31 absent scene usable; evaluation chưa được mở |

Hai nhóm pair thông thường lấy từ official XQLFW protocol, đã kiểm nhất quán metadata và điều kiện detector; **không tuyên bố đã kiểm trực quan từng pair**. Scene được self-confirm từ contact sheet, không có người gán nhãn độc lập. Các identity ở development và evaluation **không giao nhau** trên cả pair và scene; số identity nguồn sau khóa tương ứng 1.807 và 435. Các pair/trial dùng chung identity trong *cùng* split nên không được xem là quan sát thống kê độc lập; khi báo khoảng bất định phải xét cluster theo identity/anchor.

## Định nghĩa hard negative sau khóa nhãn

Trên **target-absent scene usable** có reference A và hai panel B/C đã biết khác A, chạy P2 với detector/encoder và `τ=0,147897`, `δ=0,076473` **đã cố định từ T-017**. Nếu P2 chọn một box, `A_ref ↔ selected non-target box` là **S4-derived hard-negative pair**. Nếu P2 unresolved, trial vẫn nằm trong mẫu số S4 absent/unresolved nhưng **không** thành pair đã tới S8. Output/score P2 chỉ quyết định *một negative nào được S4 chuyển tiếp*; identity âm tính đã khóa từ nguồn, P2 không tạo ground truth. Không dùng score cao để chọn thủ công, không sửa nhãn khi thấy lỗi. Với development, số hard negative sẽ được báo sau khi chạy; với evaluation, vẫn ẩn cho đến khi khóa rule nghiên cứu trên development.

## Khóa tái lập và nơi giữ artifact

| Artifact / input | SHA-256 hoặc seed |
|---|---|
| XQLFW ZIP | `1af459679fba23a12f4d83c82a81523eb930a4aec759eebefcbdde69a678962c` |
| XQLFW official pairs | `636852f90b886f3f56c73b13c9775f7ffcd37662dbb189c694f6a0a605b63b84` |
| T-014 identity split | `23542240bcc7b5d852ed469a35180dd7e68ae18942390bba25dc9106946692e2` |
| T-015 scene manifest | `ae80423e479d616052a2bf2cc5a24d2dd45519bb12957525e33f8ab45b769c74` |
| T-017 scene manifest | `5ca44481ce26abe62e2e699bdaae44c7b9227f2a5c54f6ac9d865330ad658290` |
| Detector pack | `57d31b56b6ffa911c8a73cfc1707c73cab76efe7f13b675a05223bf42de47c72` |
| Construction seed | `T-022-controlled-two-face-v1` |
| Candidate manifest | `9a200393e017f8e5a4be6fd13f16d8101f1c84b47e7fb166837c7e5f76f38c83` |
| Detection-only audit | `721782910733e37bfb93e042bc828ad6cf7b7dc3ca2b19574f1229f315745e33` |
| **Locked benchmark manifest** | **`d752c99fae5071c2aedb7fe0e40842b8b25c05decf539b61df8e988fee8ec131`** |

Script tái lập: `scripts/t022_construct_controlled_s8.py`, `scripts/t022_detector_audit.py`, `scripts/t022_review_sheets.py`, `scripts/t022_lock_benchmark.py`. Manifest JSON, ảnh ghép, contact sheet và box từng sample nằm ngoài Git tại `%TEMP%/T-022-controlled-s8-v1/` và `%TEMP%/T-022-controlled-s8-review-v1/`; **không commit ảnh mặt, identity, embedding, raw score hoặc output lớn**. Để tái lập trên máy khác, cần các asset nguồn có hash trên và chạy script theo đúng thứ tự. `%TEMP%` có thể bị dọn; trước khi chuyển máy phải lưu riêng artifact theo quy định nhóm.

## Giới hạn và bước tiếp theo

Đây là ảnh người nổi tiếng/ảnh công khai ghép thành hai panel, không mô phỏng ánh sáng, camera, chuyển động, khoảng cách, thao tác khai hồ sơ hay tần suất người nền của cửa phòng thi. Một người tự kiểm trực quan, **không có independent reviewer**; ảnh mờ và nhãn nguồn có thể còn sai. Lọc detector và visual làm tập nhỏ, thiên về trường hợp dễ quan sát. Hard negative có thể rất ít; nếu P2 không chọn đủ absent scene, không suy ra risk bound mạnh. `2/41` của T-017 và mọi tỷ lệ ở đây không phải real-world FAR.

**Bước kế tiếp được phép:** chỉ trên **development**, chạy cùng encoder/cosine, báo phân bố genuine, ordinary impostor và hard negative, cùng FNMR/FMR theo nhiều operating point, tỷ lệ S4 correct/wrong/unresolved. Vì acceptable false-accept risk demo vẫn `TBD`, chưa chọn ngưỡng tối ưu/triển khai. Nếu cần một numeric threshold để mở frozen evaluation, **đề xuất rule research/reference sau khi xem đầy đủ trade-off development**, giải thích tính trung lập, cho Quốc An review rồi mới khóa. Không dùng evaluation để chọn rule, thay nhãn, loại sample sai hoặc tune P2.
