# T-017 — Xác nhận sạch S4 trên holdout XQLFW

**Ngày chạy:** 2026-09-29. **Người thực hiện:** Quốc An (Codex hỗ trợ). **Trạng thái:** clean confirmation đã chạy một lần, nhãn và tham số khóa trước score; quyết định ở cuối chỉ áp dụng cho hướng nghiên cứu. **Nguồn:** [protocol T-017](T-017-clean-confirmation-protocol.md) ← [phân tích T-016](T-016-comparison-ablation.md) ← [protocol T-014](../04-optimization/T-014-method-protocol.md). Đây là proxy **chọn mặt S4**, không phải check-in hoặc verification 1:1 S8.

## 1. Vì sao cần run này và điều gì đã khóa

T-015 cho thấy P2 tăng số ca target-present được chọn so với B0, nhưng vẫn chọn một mặt ở 2/35 trial target-absent. T-016 nhận ra điểm mục tiêu T-015 lấy từ box detector, trái thứ tự point-first T-014. T-017 kiểm xu hướng đó trên **holdout identity nguồn chưa dùng** với điểm thị giác trên ảnh gốc trước khi xem box, không mở phương pháp mới.

| Mốc theo thứ tự | Bằng chứng khóa |
|---|---|
| Protocol/chọn holdout trước score | Commit `4d8c1be`; split T-014 SHA `23542240…6692e2`; scene manifest SHA `5ca44481…658290`. |
| Ảnh gốc không box/score → điểm visual → R50 audit-only | Visual review SHA `c19136db…a0d728`; nhãn cuối SHA `130408bd…dc7d11`; commit `50668fe` ghi hash và audit trước candidate score. Không có người gán nhãn độc lập. |
| Code confirmatory và cấu hình trước score | Commit `fe8fa2d`; T-015 frozen config SHA `a63f64d7…ff7980d`; `τ=0,14789717107158995`, `δ=0,07647264965285691`. |
| Một lượt holdout | Raw SHA `dceea1ab…9811c8`; runner SHA `7f9fc57e…4550a2`. Không tune hoặc sửa nhãn sau output. |

Giữ cùng nguồn JPG XQLFW, SCRFD-500MF detector input 640×640/detection threshold 0,5, MobileFaceNet `buffalo_sc`, crop 112×112, cosine và CPU provider. P1 luôn chọn top score khi không hòa; P2 chỉ chọn nếu đồng thời qua `τ` và gap top-2 qua `δ`. B0/A0 không chọn khi có ≥2 detection. R50 chỉ kiểm chéo nhãn trước score MBF, không tham gia lựa chọn P1/P2. Các file ảnh, identity, điểm, score và raw từng trial ở Temp ngoài Git; đường dẫn/hashes trong [handoff](../handoffs/T-017-s4-clean-confirmation.md).

## 2. Holdout và mẫu số

Từ 1.116 identity evaluation của T-014, loại mọi identity nguồn từng xuất hiện ở pilot hoặc scene/present/absent reference T-015. Còn **994 identity evaluation chưa dùng**. Duyệt thứ tự seed T-017 cố định: 618 ảnh, 554 ảnh có 0/1 detection, chọn đủ **64 scene** có ≥2 detection, genuine reference và tối đa một scene/identity. Tất cả identity **được biết qua folder nguồn** của holdout tách khỏi development, pilot và evaluation cũ. Identity người nền XQLFW không được gán đầy đủ nên không thể chứng minh tách tuyệt đối cho họ.

| Audit 64 scene | Số cảnh / trial | Cách hiểu |
|---|---:|---|
| Visual nhiều người và target rõ | 57 scene | Điểm tâm ghi từ ảnh gốc không vẽ box. |
| Visual ambiguous | 5 scene | Không ép nhãn. |
| False extra detection | 2 scene | Có ≥2 box nhưng không đủ hai người thật rõ; loại khỏi phép so nhiều người. |
| Present usable sau metadata, box và R50 | **49/64** | 15 không vào mẫu số present. |
| Absent usable sau metadata, box và R50 | **41/64** | 23 không vào mẫu số absent. |
| Target nhìn thấy nhưng không box chứa điểm | **2/64** | Giữ trong audit (`holdout-008`, `holdout-055`), không chấm như lỗi riêng của S4. |

Lý do audit có thể chồng nhau: present reference không đúng một detection (6), absent reference không đúng một detection (12), R50 present rank conflict (1), R50 absent relative conflict (1), cùng visual/box issues trên. Không loại một trial vì P1/P2 sai. Cả hai mẫu số usable đều vượt mức tối thiểu 30 của T-014, nhưng kết luận vẫn **conditional on self-confirmed proxy**. Mỗi scene có thể tạo một present và một absent trial; 90 trial usable không phải 90 scene độc lập.

## 3. Kết quả paired của một lượt holdout

| Target-present, N=49 | Chọn đúng | Chọn sai | Chưa kết luận |
|---|---:|---:|---:|
| B0/A0 | 0 | 0 | 49 |
| P1 top-1 | 49 | 0 | 0 |
| P2 selective, tham số cũ | **46** | **0** | **3** |

| Target-absent, N=41 | Không chọn mặt | Chọn một mặt sai |
|---|---:|---:|
| B0/A0 | 41 | 0 |
| P1 top-1 | 0 | 41 |
| P2 selective, tham số cũ | **39** | **2** |

P2 chuyển **46/49** present từ unresolved ở B0 sang chọn đúng, nhưng tạo **2/41** false-selection absent mà B0 không có. So với P1, P2 giữ unresolved ba present P1 chọn đúng và tránh chọn sai ở **39/41** absent. Trên holdout này không có wrong-target present ở P1 hoặc P2. Tỷ lệ P2 correct present **46/49 = 93,9%** (Wilson 95% khoảng 83,5–97,9%); false-selection absent **2/41 = 4,9%** (khoảng 1,3–16,1%). `0/49` wrong-target present không chứng minh lỗi thực bằng 0 (giới hạn trên Wilson khoảng 7,3%). Không cộng hai nhóm thành một “accuracy hệ thống”.

**Theo số detection:** present usable có 40 scene hai mặt (P2 37 đúng/3 unresolved), 7 scene ba mặt (7/0), 2 scene bốn mặt (2/0). Absent usable có 35 scene hai mặt (P2 34 không chọn/1 false), 5 scene ba mặt (5/0), 1 scene bốn mặt (0/1). Số scene ba/bốn mặt quá nhỏ để suy xu hướng riêng.

## 4. Ca lỗi còn lại và mức giải thích

| Trial | Nhóm | P1 → P2 | Top cosine | Gap top-2 | Giải thích trực tiếp từ quy tắc đã khóa |
|---|---|---|---:|---:|---|
| `holdout-030` present, 2 mặt | P2 unresolved | đúng → không chọn | 0,114172 | 0,109361 | Top dưới `τ`; gap qua `δ`. |
| `holdout-034` present, 2 mặt | P2 unresolved | đúng → không chọn | 0,140392 | 0,077674 | Top dưới `τ`; gap vừa qua `δ`. |
| `holdout-038` present, 2 mặt | P2 unresolved | đúng → không chọn | 0,032402 | 0,017961 | Cả top và gap dưới ngưỡng. |
| `holdout-010` absent, 4 mặt | P2 false-selection | sai → sai | 0,238723 | 0,124619 | Hai điều kiện đều qua; P2 chọn box 3 theo nhãn absent proxy. |
| `holdout-018` absent, 2 mặt | P2 false-selection | sai → sai | 0,156472 | 0,166434 | Hai điều kiện đều qua; top chỉ cao hơn `τ` khoảng 0,0086. |

Ba present unresolved đều có target box trong nhãn đã khóa; hiện **không** có bằng chứng chúng do detector bỏ sót. Hai absent false-selection là lỗi **chọn mặt S4 theo nhãn proxy**, chưa phải false accept ở S8; hệ thống thực còn bước xác minh 1:1 và quyết định nghiệp vụ. Score/gap giải thích vì sao rule P2 chọn hoặc từ chối, **không chứng minh** nguyên nhân sâu là ánh sáng, crop hay encoder. Không sửa nhãn của hai absent sau khi thấy output; identity người nền chưa đầy đủ vẫn là giới hạn của cả hai nhãn.

## 5. Chi phí, so T-015 và giới hạn

Trên runner Windows 11, Python 3.12.2, 12 logical CPU, OpenCV 5.0.0, ONNX Runtime 1.20.1, InsightFace 0.7.3, NumPy 2.2.6, CPUExecutionProvider, model warm/cache trên đĩa: scene decode+detect median/p95 **14,09/21,08 ms** (90 trial); embedding từng mặt scene **8,20/12,73 ms** (198 lượt); reference decode+detect **14,33/23,25 ms** (90); reference embedding **8,43/13,29 ms** (90). Quyết định P1/P2 sau score median **0,0042/0,0010 ms**. Đây là thời gian **thành phần**, không cộng các median thành latency đầu-cuối và không so trực tiếp với T-015 ở trạng thái tải CPU khác hay thiết bị cửa phòng.

| Xu hướng cùng cấu hình P2 | T-015 evaluation | T-017 holdout sạch | Diễn giải |
|---|---:|---:|---|
| Present đúng / wrong / unresolved | 35/0/6, N=41 | **46/0/3, N=49** | Cùng xu hướng P2 tăng coverage so B0, vẫn còn unresolved. Khác mẫu, không gọi mức tăng 85,4% → 93,9% là cải thiện model. |
| Absent không chọn / false-selection | 33/2, N=35 | **39/2, N=41** | **False-selection lặp lại** với tham số frozen. |
| P1 absent false-selection | 35/35 | 41/41 | Hệ quả cơ học của ép top-1 ở cảnh có ≥2 detection. |
| Điểm target trước box | Không: điểm lấy từ box đã nhìn | Có: điểm trên ảnh gốc trước khi nối box | Audit mới bắt được 2 ca target không có box chứa điểm; không thể định lượng bias T-015 chỉ từ hai holdout khác nhau. |

Giới hạn quan trọng: self-confirm một người; R50 filter có thể thiên về ca dễ cho embedding; 15 present/23 absent không vào mẫu số; absent reference không có nhãn đầy đủ cho người nền; XQLFW là ảnh web, không phải camera cửa phòng; target-present/absent là proxy tạo từ reference, không là lượt khai mã; chưa chạy verification S8 sau selection, chưa có thiết bị đích hoặc policy của một kỳ thi. Holdout mới tách identity nguồn được biết, không khẳng định mọi khuôn mặt nền tách nhau. Không dùng các tỷ lệ này làm cam kết vận hành.

## 6. Quyết định T-017 và hệ quả

**Chọn: tiếp tục giữ selective S4 là hướng ứng viên, chưa triển khai/chốt P2 với `τ,δ` này làm cấu hình cuối.** Lý do: P2 lặp lại lợi ích lớn về chọn đúng present so với B0 và tránh hầu hết absent false-selection của P1, nhưng vẫn false-select **2/41 absent** trên holdout point-first, trong khi nhãn absent và domain còn giới hạn. Chưa có bằng chứng buộc thiết kế S4 khác; cũng chưa có căn cứ gọi P2 an toàn cho app thật. B0 vẫn là đường fallback `unresolved` trong nhiều mặt.

**Bước tiếp theo phát sinh từ quyết định:** nếu tích hợp bản demo, giữ S4 ở chế độ nghiên cứu/không tự cấp quyền vào phòng; mọi mặt được chọn phải qua S8 1:1 và rule/authority của app, `unresolved` chuyển review. Để chốt triển khai cần kiểm end-to-end S4→S8 trên nguồn có nhãn absent/background tốt hơn hoặc một giao thức proxy ghi rõ giới hạn, đo trên thiết bị đích và quy tắc chấp nhận theo nghiệp vụ. Không dùng holdout này để chỉnh `τ,δ`; nếu thử cải tiến mới phải mở task/protocol mới và holdout khác.
