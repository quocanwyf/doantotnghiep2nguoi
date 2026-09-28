# Giai đoạn 05 — đánh giá

Ghi tài liệu so sánh theo task khi có số liệu: baseline, proposed, chênh lệch, độ biến thiên giữa các run, điều kiện đo và giới hạn kết luận. Nếu có nhiều cải tiến, bổ sung ablation để tách tác động.

Mỗi run có một file theo [RUN-TEMPLATE.md](RUN-TEMPLATE.md). Không kết luận “tốt hơn” khi metric, split hoặc điều kiện đo khác nhau mà chưa giải thích.

## Đầu ra hiện có

- [T-016 — so sánh và phân tích lỗi S4](T-016-comparison-ablation.md): replay mô tả B0/P1/P2 từ output T-015 đã khóa; có paired counts, gate ablation, sample lỗi và giới hạn nhãn. Chưa là quyết định triển khai cuối.
- [Logic quyết định giai đoạn 05](DECISION_LOGIC.md) nối bằng chứng T-015/T-016 với việc cần xác nhận trước T-017.
