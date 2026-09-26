# Bàn giao T-011 — run E2 thăm dò, các nhánh khác còn mở

- **Người thực hiện/ngày:** Codex theo yêu cầu Quốc An, 2026-09-26; Minh Hy là người review theo Sheet.
- **Nguồn đầu vào:** Quốc An cho phép dùng T-008 làm baseline tạm để tiếp tục; PR #3 thực tế vẫn có review CHANGES_REQUESTED của Hy. Xem [rà soát đầu vào](../03-baseline/T-011-readiness-review.md). T-009 PR #5 và T-010 PR #6 chưa merge vào main.
- **Đầu ra:** [run E2 XQLFW/MobileFaceNet](../03-baseline/runs/T-011-E2-xqlfw-mbf.md), mã scripts/t011_xqlfw_baseline.py và ba unit test trong tests/test_t011_protocol.py. T-011 chưa hoàn tất toàn bộ E1/E2/E3/M1.
- **Cách kiểm:** dùng Python 3.12.2 với InsightFace 0.7.3, OpenCV runtime 5.0.0, ONNX Runtime 1.20.1 CPU, NumPy 2.2.6 và scikit-learn 1.7.1. Chạy unittest discover trên tests/test_t011_protocol.py (3 test qua); chạy script với XQLFW ZIP, pairs TXT và buffalo_sc ZIP có hash trong run doc. Script xuất JSON tổng hợp vào artifacts, không xuất tên/ảnh/embedding.
- **Kết quả:** 7.263 ảnh được tham chiếu, 6.064 ảnh tạo embedding đúng một mặt; 4.215/6.000 cặp hợp lệ; FMR 133/2.169 = 6,13%, FNMR 125/2.046 = 6,11% tại threshold chọn trên 9 fold khác. Đây là phép thử pair-fold học thuật, không có identity-disjoint hoặc kết quả cửa phòng thi.
- **Việc tiếp theo:** T-012 phân tích 908 ảnh detector báo nhiều mặt và 291 ảnh không phát hiện để đặt giả thuyết coverage; kiểm một encoder khác trên cùng protocol; tìm main test phù hợp hơn. E1 cần archive/nhãn detection; E3 cần giải quyết ý review T-008 và implementation; M1 cần điều kiện đo kiểm soát. Không chốt model/threshold cuối từ run này.
- **File ngoài Git:** XQLFW ZIP/pairs, buffalo_sc ZIP, ONNX giải nén và JSON run ở máy chạy; nguồn và hash trong [external-assets](../00-project/external-assets.md). Chưa gửi trực tiếp cho Minh Hy; tải lại từ nguồn công khai và đối chiếu hash.
- **Commit/PR:** commit mã run 03c68d6; PR T-011 được gắn sau khi push nhánh. Không merge khi các giới hạn trên chưa được nhóm hiểu rõ.
