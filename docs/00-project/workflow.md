# Quy trình phối hợp qua Sheet và GitHub

Nhóm gồm **Quốc An (TV-A)** và **Minh Hy (TV-B)**. Hướng dẫn để Minh Hy bắt đầu trên máy riêng ở [onboarding.md](onboarding.md).

## Hai nguồn dùng cho hai mục đích

- [Google Sheet task](https://docs.google.com/spreadsheets/d/14BQCQ_LbGkZS15Grfi4AZNWBX15h479XjoyQvP9jHcU/edit?gid=0#gid=0): mã việc, người làm chính, người review, trạng thái, hạn, trở ngại và link đầu ra.
- [GitHub repo](https://github.com/quocanwyf/doantotnghiep2nguoi): mã, kiến thức dự án, quyết định, kết quả và note bàn giao. Không tạo task board thứ hai trong repo.

## Hai vòng đề xuất song song

Ở giai đoạn 01 và 02, Quốc An và Minh Hy mỗi người có **task và file đề xuất riêng**. Cả hai cùng nghiên cứu đầy đủ vấn đề, sau đó trình bày, hỏi chéo và chọn một phương án chính có lập luận/bằng chứng tốt hơn. Không gộp hai bản nháp thành quyết định trước buổi trao đổi. Người phụ trách task chọn phương án ghi lại kết luận; người còn lại review; cả hai phải đồng ý trước khi đánh dấu đã chốt trong nhóm. Các điểm cần thầy xác nhận vẫn ở `questions.md`.

## Một vòng làm việc

1. **Nhận việc:** đồng bộ `main` mới nhất (`git pull --ff-only`), xem task ID trên Sheet, đọc `AGENTS.md`, `status.md`, quyết định, note bàn giao và tài liệu giai đoạn liên quan. Mỗi task có một người phụ trách chính và một người review.
2. **Làm:** tạo nhánh ngắn gắn task ID, ví dụ `task/T-001-problem-scope`. Ghi cấu hình, nguồn và kết quả ngay trong tài liệu liên quan. Nếu phát sinh lựa chọn quan trọng, lập đề xuất quyết định để hai người xem; không tự coi nó là đã chốt.
3. **Bàn giao:** cập nhật tài liệu cùng mã; tạo `docs/handoffs/T-001-ten-ngan.md` theo mẫu. Ghi việc đã làm, cách chạy/kiểm tra, commit hoặc PR, điều còn vướng và file ngoài Git cần trao riêng. Nếu có file ngoài Git, thêm vào `external-assets.md`.
4. **Review và hợp nhất:** push nhánh, gửi PR cho người còn lại review. Sau khi gộp vào `main`, cập nhật dòng task trên Sheet bằng trạng thái và link PR/commit/tài liệu. Người kia pull `main` rồi đọc note bàn giao trước khi làm tiếp.
5. **Cuối tuần:** cả hai cập nhật chung một file `docs/progress/YYYY-Www.md`; sửa `status.md` nếu mốc hoặc rủi ro chung thay đổi.

Nếu chưa dùng PR, ít nhất hai người cần đồng bộ `main` trước khi sửa và review thay đổi quan trọng trước khi push. Tránh hai người cùng sửa một file chung trong thời gian dài.

## Điều kiện bàn giao xong

- Kết quả có đường dẫn và cách kiểm tra/tái lập.
- Tài liệu không mâu thuẫn với quyết định hoặc trạng thái hiện tại.
- Task trên Sheet dẫn tới đúng kết quả.
- Mọi file bị `.gitignore` chặn nhưng cần cho người kia đã có mục bàn giao và tình trạng gửi/nhận.

## Ghi logic quyết định theo tiến độ

Khi bắt đầu một giai đoạn, tạo hoặc cập nhật DECISION_LOGIC.md ngay trong folder đó **cùng lúc với việc đang làm**, không lập trước file rỗng cho các giai đoạn tương lai. File giải thích vì sao bước tiếp theo tồn tại và được suy ra từ bước trước theo chuỗi: Business Problem → Problem Decomposition → Stage Requirements → Data/Technical Requirements → Survey → Candidate Selection → Experiment → Final Technical Decision → Implementation.

Ở Survey, quyết định chỉ là candidate đủ phù hợp để đem thử dựa trên requirement và bằng chứng khảo sát. Experiment kiểm chứng uncertainty còn lại bằng câu hỏi, biến, điều kiện kiểm soát, dữ liệu/split, metric và tiêu chí chấp nhận đã định trước; kết quả mới hỗ trợ quyết định kỹ thuật cuối. Nếu chưa có bằng chứng hoặc nhóm chưa thống nhất, ghi rõ trạng thái mở. DECISION_LOGIC.md là bản đồ lập luận và liên kết, không sao chép deliverable chính hoặc thay thế quyết định chính thức trong docs/00-project/decisions/.
