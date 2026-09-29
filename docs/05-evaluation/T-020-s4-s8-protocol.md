# T-020 — Giao thức kiểm tích hợp S4 → S8

**Ngày khóa thiết kế:** 2026-09-29. **Người phụ trách:** Quốc An. **Trạng thái:** giao thức trước lượt S8. Đầu vào S4 là raw holdout T-017 đã khóa, không chạy lại detector/encoder, sửa nhãn, `τ`, `δ`, hay output B0/P1/P2.

## Câu hỏi và ranh giới

T-017 cho thấy P2 chọn đúng 46/49 target-present và chọn nhầm một mặt ở 2/41 target-absent. T-020 hỏi: khi mặt P2 đã chọn đi qua S8 xác minh 1:1, S8 chặn được bao nhiêu lỗi chọn mặt đó, và đổi lại từ chối bao nhiêu mặt đúng? Đây là proxy XQLFW nhiều mặt, không phải lượt khai mã tại phòng thi hoặc quyết định cho vào phòng.

**S4 `UNRESOLVED` → không gọi S8.** App có thể yêu cầu thử lại, hướng dẫn đứng một mình trong vùng camera, hoặc chuyển người có thẩm quyền kiểm thủ công. Kết quả S8 `ACCEPT` chỉ là tín hiệu xác minh; quyền vào phòng và attendance vẫn do policy/quy trình nghiệp vụ quyết định.

## Ngưỡng S8 chỉ từ development

1. Dùng pair protocol XQLFW đã kiểm SHA trong T-011 và split danh tính T-014 SHA `23542240bcc7b5d852ed469a35180dd7e68ae18942390bba25dc9106946692e2`. Chỉ giữ pair mà **cả hai identity nguồn** nằm trong `development`; không dùng identity `evaluation`, pilot hay score T-017. Ghi số genuine/impostor và số pair bị loại vì detector trả về 0 hoặc >1 mặt.
2. Dùng đúng SCRFD-500MF + MobileFaceNet `buffalo_sc`, input detector 640×640, `det_thresh=0.5`, crop encoder 112×112, CPUExecutionProvider và cosine như T-011/T-017. Chỉ tính pair khi mỗi ảnh có đúng một mặt. Không thay dữ liệu hoặc nhãn theo kết quả.
3. Chọn **một** ngưỡng bằng hàm `select_threshold` đã có ở `scripts/t011_xqlfw_baseline.py`: giảm `|FMR−FNMR|` trên development, hòa thì ưu tiên FMR thấp hơn, rồi ngưỡng cao hơn. Đó là điểm cân bằng mô tả nghiên cứu, **không phải policy an toàn kỳ thi**. Lưu config và hash trước khi đọc raw T-017 cho S8. Không chỉnh ngưỡng bằng holdout.

## Một lượt nối S4 → S8 trên holdout T-017

- Kiểm SHA raw T-017 `dceea1abe0d09e78479473bc28a068f2b32d601c840cff0fceac09e1419811c8`, nhãn `130408bd8f7a02ce502f31cb8f386a01d7adfeab9d5be00bc8fe9a195adc7d11` và frozen P2 `a63f64d7fa6cfe4d3d98f2d52c10a30d7bb8445b20de8b0e6b4780ff1ff7980d`.
- Cho B0/P1/P2 qua cùng quy tắc S8 để so paired. Nếu S4 có `selection`, S8 so cosine **đã tính ở chính box đó** với ngưỡng development. Nếu không chọn, ghi `UNRESOLVED` và không tạo quyết định S8. Đây là phép **replay của cùng embedding**; S8 không phải mô hình độc lập và không cộng thêm một lượt encode vào runtime.
- Nhãn present + box đúng là genuine cho phép đo S8 có điều kiện; present + box sai hoặc absent + box bất kỳ là impostor theo proxy nhãn T-017. Absent có người nền chưa được gán danh tính đầy đủ nên kết luận false accept là **theo proxy**, không phải bằng chứng chắc chắn người nền khác hồ sơ.
- Báo riêng `S4 đúng + S8 accept`, `S4 đúng + S8 reject`, `S4 sai + S8 reject`, `S4 sai + S8 accept`, `S4 unresolved`; target-absent `không chọn`, `chọn + reject`, `chọn + accept`. FMR/FNMR S8 dùng **mẫu số các trial thực sự đi vào S8**, không trộn unresolved vào mẫu số. Báo N present/absent, số scene hữu dụng, số detection, và raw per-sample ngoài Git. `S4 sai + S8 accept` là lỗi nguy hiểm của pipeline proxy; `S4 sai + S8 reject` là lỗi S4 được S8 chặn. Không gọi riêng lỗi chọn mặt là false accept S8.
- Không dùng holdout để tune S4/S8, loại sample sai, sửa ground truth hoặc chọn lại family. Chỉ một lượt S8 trên raw holdout đã khóa.

## Quyết định sau phép đo

Chỉ kết luận selective S4 **đáng tiếp tục làm front end nghiên cứu** nếu số ca đúng và những lỗi còn lại được báo với mẫu số rõ ràng. Không chốt ngưỡng/cấu hình triển khai nếu có false accept proxy, thiếu nhãn người nền, thiếu dữ liệu camera và thiết bị đích hoặc chưa có tiêu chí chấp nhận nghiệp vụ. Nếu S8 dùng cùng cosine với S4, cần xem rõ sự phụ thuộc: hai ngưỡng không tạo hai tín hiệu nhận dạng độc lập.
