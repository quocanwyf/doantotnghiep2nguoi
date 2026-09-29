# T-017 — Clean confirmation S4 trên holdout chưa xem

**Trạng thái:** protocol khóa trước khi dựng holdout/đọc score candidate. **Nguồn quyết định:** T-014 quy định nhãn điểm trên ảnh gốc; T-016 chỉ ra T-015 đã lấy điểm từ box và chưa đủ bằng chứng chốt P2. **Phạm vi:** proxy XQLFW cho chọn mặt S4; không phải lượt check-in, quyền vào phòng hay xác minh 1:1.

## Câu hỏi và cấu hình cố định

Kiểm xem xu hướng B0/P1/P2 ở T-015 có lặp lại trên identity/scene chưa dùng, khi điểm mặt mục tiêu được ghi **trực tiếp trên ảnh gốc trước khi xem box**. Chỉ thử B0/A0 (nhiều detection thì unresolved), P1 top cosine và P2 với `τ=0.14789717107158995`, `δ=0.07647264965285691`. Giữ nguyên XQLFW, SCRFD-500MF 640×640 threshold detector 0,5, crop 112×112, MobileFaceNet `buffalo_sc`, cosine và CPU runner T-015. Không tune, đổi candidate, thay nhãn theo output hay chạy lại holdout để cải thiện điểm.

## Chọn holdout trước score

Đọc đúng split T-014 SHA-256 `23542240bcc7b5d852ed469a35180dd7e68ae18942390bba25dc9106946692e2`. Chỉ lấy identity thuộc **evaluation** T-014. Loại mọi identity xuất hiện ở scene, present reference hoặc absent reference của **cả hai split T-015**, cùng pilot T-013. Sắp scene còn lại theo SHA-256 của `T-017-clean-scenes-v1\0<member>`; chọn 64 scene đầu có genuine neighbor, ≥2 detection B0, tối đa một scene/identity nguồn. Present reference là genuine neighbor đầu tiên theo `T-017-present-v1`; absent reference là ảnh đầu tiên thuộc identity khác trong tập được phép theo `T-017-absent-v1\0<scene>`. Không thay thế scene/reference sau khi xem ảnh, audit hoặc score. Nếu không đủ 64, báo số thực.

Nhãn nguồn chỉ định identity của người chính trong ảnh, không định danh đầy đủ mọi người nền. Vì vậy identity-disjoint được bảo đảm cho identity **đã biết**; trường hợp người nền không biết danh tính là giới hạn. Holdout có một trial present và một absent trên mỗi scene, hai trial phụ thuộc cùng cảnh.

## Khóa nhãn hai bước

1. Tạo ảnh review **không vẽ detector box, không hiện score**. Đối chiếu reference và ảnh scene. Với present, chỉ khi xác định được người mục tiêu bằng mắt thì ghi `target_center_normalized=[x/W,y/H]` trên ảnh gốc; không ghi box index ở bước này. Với absent, chỉ ghi `appears_absent_unverified` khi không thấy người trong reference ở scene. Nếu nhiều người khó phân biệt, ảnh mờ, reference sai hoặc không chắc absent, ghi `AMBIGUOUS`. Khóa file điểm thị giác bằng hash trước khi mở box/score.
2. Audit byte/metadata/genuine pair; nối điểm với **duy nhất một** box B0, kiểm detector ổn định và reference đúng một mặt. Không box chứa điểm → `TARGET_MISSED_BY_DETECTOR`; nhiều box → `AMBIGUOUS`. R50 chỉ là cross-check phụ giống T-014: present target phải xếp đầu, absent max R50 thấp hơn positive anchor cùng scene. Bất đồng → `AMBIGUOUS`, không sửa điểm để hợp model. Khóa label manifest/hash **trước khi** đọc MobileFaceNet score B0/P1/P2.

Chỉ một người self-confirm, không có reviewer độc lập. Ca `AMBIGUOUS` không vào mẫu số hiệu quả, vẫn báo số và lý do. Không loại ca vì P1/P2 sai.

## Chạy, mẫu số và quyết định

Chỉ sau khi label manifest khóa, chạy B0/P1/P2 **một lần** trên mọi trial usable cùng input và cấu hình đã cố định. Lưu raw theo sample ngoài Git. Báo trong 64 scene: true multi-person, false extra, ambiguous, target-missed, usable/excluded; tách present/absent. Present: correct/wrong/unresolved; absent: no-face-selected/false-selection; số mặt và runtime median/p95 trên cùng CPU. Không gọi false-selection S4 là false accept S8. Chỉ gọi phép xác nhận định lượng có ích nếu ≥30 present và ≥30 absent self-confirm; nếu thấp hơn, báo exploratory và chưa chốt.

So paired với T-015/T-016: xu hướng đúng/lỗi/unresolved, hai absent false-selection và sáu present unresolved cũ có lặp **kiểu lỗi** hay không; không đòi cùng sample. Đưa một trong ba quyết định có điều kiện: chốt P2 cho pipeline thử, giữ selective S4 nhưng chưa triển khai, hoặc cần thiết kế S4 khác. Không suy ra hiệu quả camera phòng thi, quyền vào phòng hay attendance từ proxy này.

**Ranh giới lưu trữ:** ảnh khuôn mặt, tên nguồn, nhãn từng ảnh, embedding và raw score ở Temp ngoài Git; Git chỉ chứa protocol, script, hash, số đếm và diễn giải không định danh.
