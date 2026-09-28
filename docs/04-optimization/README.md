# Giai đoạn 04 — optimization

[T-013 — kiểm tính khả thi S4 và chọn điểm cải thiện](T-013-target-selection.md) nối lỗi B0 với câu hỏi có thể chấm bằng ảnh công khai. [Logic quyết định phase 04](DECISION_LOGIC.md) ghi vì sao bước T-014 tồn tại; T-013 chưa chọn cách chọn mặt, model hoặc thuật toán tối ưu. [Quy trình self-confirm T-013](T-013-self-confirm-protocol.md) kiểm metadata nguồn, ảnh gốc và embedding phụ trợ; không có người gán nhãn độc lập. Pilot chỉ là development.

Khi hướng được nhóm duyệt, T-014 ghi `T-014-method-protocol.md`: thành phần pipeline được tối ưu, biểu diễn nghiệm/search space, objective function, ràng buộc, thuật toán, budget tìm kiếm và vị trí chạy ở training hoặc inference.

Không gọi thay optimizer huấn luyện (Adam/SGD) hoặc bỏ layer thủ công là đóng góp optimization nếu không có bài toán tìm kiếm/quyết định rõ ràng. Ghi rõ proposed khác baseline ở đâu để đánh giá công bằng.
