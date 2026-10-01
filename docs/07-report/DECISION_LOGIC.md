# Decision logic — Tổng hợp báo cáo

## T-024: tổng hợp reasoning và slide (2026-10-01)

**Context:** nhóm đã có evidence baseline, S4, S8 và policy demo; cần báo cáo với thầy và bàn giao app mà không biến các task thành các kết quả rời rạc.

**Question:** vì sao chọn bài toán, vì sao nghiên cứu hai stage, cải thiện bằng evidence nào và vì sao giờ chuyển sang app?

**Requirements:** trace observation → question → protocol → evidence → decision; số liệu có mẫu số; giữ kết quả S4, S8 và kết hợp riêng; báo cáo10–12 phút, academic, diagram/chart/table editable, có lời nói và Q&A.

**Alternatives:** một accuracy tổng sẽ trộn benchmark; sao chép toàn report sẽ khó trình bày. Chọn một master narrative có link nguồn và deck ngắn có appendix.

**Evidence:** T-017 clean selection; T-020 replay reuse score/lower threshold; T-022 thiếu conditional hard negatives ở evaluation; T-023 benchmark độc lập cho thấy useful separation nhưng còn acceptance; D-004–D-008 chốt policy/app-first.

**Decision:** tổng hợp [T-024 research logic](T-024-research-logic.md), PowerPoint và [slide notes](T-024-slide-notes.md), không tạo experiment/model task mới. Chart S4 dùng cùng T-017 benchmark; S8 và combined dùng T-023, không nhân/ghép accuracy giữa dataset.

**Why:** người đọc cần biết bước tiếp theo tồn tại vì observation nào; đóng góp hiện tại thuộc selection/decision/pipeline và phương pháp kiểm chứng, không train encoder mới.

**Affects next:** dùng làm nguồn trình bày và báo cáo; Hy build/integrate theo bộ bàn giao. Final app test chỉ sau khi app chạy, freeze trước test. Không kết luận deployment risk đạt khi cap vẫn TBD.
