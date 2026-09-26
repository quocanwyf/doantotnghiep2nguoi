# Bàn giao T-009 — kiểm tra candidate dữ liệu và trọng số

- **Người làm, ngày:** Quốc An, 2026-09-26; chờ Minh Hy review.
- **Task trên Sheet:** [T-009, dòng 10](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0).
- **Commit/PR:** branch `codex/T-009-candidate-audit`; bổ sung URL PR sau khi mở.
- **File chính:** [T-009-candidate-audit.md](../02-survey/T-009-candidate-audit.md), [logic phase 02](../02-survey/DECISION_LOGIC.md), [README phase 02](../02-survey/README.md), [status](../00-project/status.md).
- **Cách kiểm tra và kết quả:** đối chiếu các URL nguồn chính thức trong audit; tải lại weight từ nguồn và so SHA-256 nêu trong tài liệu. Máy thử có OpenCV 5.0.0, ONNX Runtime 1.20.1, MediaPipe 1.0.0. YuNet, BlazeFace full-range, SCRFD-500MF và MobileFaceNet đã mở/chạy đầu vào toàn số 0; đó chỉ là smoke test file/runtime, chưa đo accuracy. Riêng file TXT protocol XQLFW đã tải/đếm 6.000 cặp; archive ảnh và các dataset khác chưa tải/parse để kiểm nhãn hoặc rights trong gói.
- **Quyết định và giới hạn:** chỉ giữ candidate có điều kiện để chuẩn bị B1/B2; chưa có main test, model thắng, threshold, metric kết quả hay triển khai thiết bị. T-008 ở PR riêng của Minh Hy; đối chiếu lại sau review.
- **Cần tiếp tục:** Minh Hy kiểm nguồn/quyền và mức chứng cứ; T-010 xác định protocol, dữ liệu/thiết bị, split và metric; hoàn thiện B0 của dataset trước khi chạy. Đối chiếu quyền từng weight nếu mục đích sử dụng thay đổi.
- **File ngoài Git:** các trọng số đã thử chỉ ở thư mục tạm máy kiểm tra, không gửi/nhận qua Git; không có ảnh mặt hay dữ liệu cá nhân được lưu vào repo. Tải lại theo nguồn + hash trong audit khi cần.
