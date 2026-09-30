# T-024 — AI rule, tình huống và retry cho demo

**Trạng thái:** `PROPOSED_DEMO_V1`, 2026-09-30; chưa freeze/kiểm nghiệm trên app. Đọc cùng [quy trình tổng](T-024-demo-decision-policy.md) và [business policy](T-024-business-policy.md). Các số 1/2/3 lấy từ đề xuất Quốc An cung cấp, không phải ngưỡng hiệu năng đã được chứng minh.

## 1. Contract sau business pre-check

Đầu vào: một claimed registration/reference đã xác định, context hợp lệ, attempt và phiên bản policy/AIConfig. Camera tạo observation; detector cung cấp candidate faces; S4 chọn candidate hoặc `UNRESOLVED`; S8 so candidate với **reference của hồ sơ đã khai**, trả `VERIFIED/NOT_VERIFIED/UNAVAILABLE`. Các nhãn component này diễn giải verdict `ACCEPT/REJECT` của phép nghiên cứu thành outcome app; không thay rule scoring hoặc biến ACCEPT thành bảo đảm đúng ground truth.

Một mặt không tự xác minh danh tính. Nhiều mặt nhưng chọn được candidate thì tiếp tục; không mặc định yêu cầu mọi cảnh chỉ có một người. Giữ nguyên phương pháp S4/S8 được freeze, không thêm bypass hoặc tune tại T-024.

[T-023](../05-evaluation/T-023-encoder-evaluation-result.md) mới kiểm ảnh tĩnh proxy với SCRFD/MobileFaceNet/cosine. Chưa có bằng chứng tất cả quality case, target stability hay retry dưới đây đã được tự phát hiện/chạy trong app. “Quality không đạt” có thể do operator nhận thấy hoặc capability sẽ triển khai; tiêu chí/method tự động còn TBD, không tự chọn thêm model.

## 2. Camera và observation

Retry ở bảng là **số lần thử thêm**, luôn chịu global budget mục 5.

| ID | Tình huống | Retry demo đề xuất | Xử lý / giới hạn |
| --- | --- | ---: | --- |
| AI-C01 | Camera không mở/permission lỗi | 1 recovery | Thử khởi tạo lại; vẫn lỗi → SYSTEM_HOLD và fallback có người xử lý. |
| AI-C02 | Không lấy được frame | 1 recovery | Reconnect/reinitialize; không có observation dùng được → MANUAL/SYSTEM_HOLD. |
| AI-C03 | Không có face detection | 2 capture | Hướng dẫn vị trí/nhìn camera; capture mới, hết ngân sách → MANUAL. |
| AI-C04 | Face quá nhỏ/xa để dùng | 2 capture | Hướng dẫn gần camera; tiêu chí usable size TBD. |
| AI-C05 | Blur/không rõ | 2 capture | Giữ yên, chụp mới; quality criterion chưa khóa. |
| AI-C06 | Quá tối/sáng | 2 capture | Điều chỉnh vị trí/ánh sáng; chưa có detector lỗi ánh sáng được xác nhận. |
| AI-C07 | Che mặt làm evidence không đủ | 2 capture | Hướng dẫn theo policy, không tự giả định giấy tờ/biometric hoặc quy định tháo đồ. |
| AI-C08 | Góc mặt không dùng được | 2 capture | Điều chỉnh hướng mặt; chưa chốt pose criterion. |
| AI-C09 | Người đang tương tác rời vị trí | 1 capture nếu tiếp tục | Quay lại để thu observation mới; bỏ lượt → INTERRUPTED. Cách nhận biết rời vị trí TBD. |

C04–C08 dùng **chung `poor_quality_retry`**, không có 5 ngân sách cộng dồn. C01/C02 dùng chung ngân sách camera recovery. Reference thiếu/sai/corrupt phải chuyển business/manual, không chữa bằng capture mới.

## 3. S4 — target selection

| ID | Tình huống | Retry demo đề xuất | Xử lý |
| --- | --- | ---: | --- |
| AI-S401 | Một face và S4 chọn candidate theo rule frozen | 0 | Sang S8; không tự coi face đó là đúng identity. |
| AI-S402 | Nhiều face và S4 chọn candidate theo rule frozen | 0 | Sang S8; MULTI_FACE không tự tạo RETRY. |
| AI-S403 | S4 unresolved | 2 capture | Hướng dẫn người khai hồ sơ đứng rõ hơn; capture mới rồi chạy lại. |
| AI-S404 | Candidate không còn evidence dùng được trước verification | 2 capture | Bỏ observation không hợp lệ, thu lại; chia sẻ ngân sách unresolved. |
| AI-S405 | Người vận hành/capability phát hiện nguy cơ target đổi hoặc selection không ổn định | 1 capture | Không ghép candidate của observation khác; thu mới. Temporal detection/tracking chưa được kiểm. |
| AI-S406 | Hết ngân sách vẫn unresolved | 0 | MANUAL; không ép chọn top-1. |

S4 “chọn được” là outcome phương pháp, không chứng minh chọn đúng. P2 selective dùng score + margin; T-023 vẫn có false selection/acceptance. Không dùng hướng dẫn “đứng rõ” để bỏ mục tiêu nghiên cứu nhiều mặt.

## 4. S8 — verification 1:1

| ID | Tình huống | Retry demo đề xuất | Xử lý |
| --- | --- | ---: | --- |
| AI-S801 | S8 đạt rule của AIConfig | 0 | AI_VERIFIED → final business-check, chưa trực tiếp ghi PASS. |
| AI-S802 | Evidence/score chưa đạt | 1 capture | Observation mới rồi S4/S8 lại; không chạy lặp score cũ để tạo cơ hội accept. |
| AI-S803 | Vẫn chưa verified hoặc hết budget | 0 | MANUAL; không suy gian lận/cấm thi. |
| AI-S804 | Lỗi xử lý candidate có khả năng phục hồi | 1 processing recovery | Thử phục hồi lỗi; vẫn lỗi → MANUAL. Reference lỗi/mapping không chắc → business/manual ngay. |
| AI-S805 | Case bất thường được báo nhưng không có rule/capability đủ kết luận | 0 | MANUAL. Đây là route ngoại lệ, không tuyên bố có model phát hiện bất thường. |

Lỗi runtime được phép thử lại cùng input khi thực sự phục hồi được processing, nhưng không tính là bằng chứng danh tính mới. S8 không đạt phải giữ verdict cũ và log recovery/capture mới.

## 5. RetryPolicy — một nguồn và ngân sách toàn attempt

Tất cả giá trị sau thuộc `ExamPolicy.RetryPolicy`, **không sao chép vào AIConfig**:

| Key | Default demo đề xuất | Đơn vị / phạm vi |
| --- | ---: | --- |
| camera_technical_retry | 1 | Recovery chung C01/C02. |
| no_face_retry | 2 | Capture bổ sung cho no-face. |
| poor_quality_retry | 2 | Capture bổ sung chung C04–C08. |
| s4_unresolved_retry | 2 | Capture bổ sung chung S403/S404. |
| s4_instability_retry | 1 | Capture bổ sung khi instability được nhận biết. |
| candidate_departure_retry | 1 | Capture bổ sung khi người quay lại. |
| s8_not_verified_retry | 1 | Capture bổ sung sau non-match/insufficient evidence. |
| processing_recovery_retry | 1 | Phục hồi lỗi xử lý, không tạo evidence mới. |
| max_capture_attempts | 3 | Initial observation + tối đa 2 capture mới cho toàn attempt. |
| manual_timeout / action | TBD | Không tự chuyển pending thành PASS hoặc vắng khi timeout. |

**Capture mới** chỉ được tạo khi còn cả ngân sách lý do và capture budget toàn attempt. **Recovery cùng input** chỉ cần recovery budget đúng loại và input còn hợp lệ; có thể phục hồi lỗi processing của capture thứ 3 dù đã hết capture budget, nhưng không được thu thêm capture thứ 4. Mọi observation được thu để kiểm, kể cả không có mặt/ảnh kém, đều tính vào capture budget. Recovery không tạo frame không tính là observation; nếu sau phục hồi camera cần frame mới thì vẫn kiểm capture budget trước khi thu. Các technical recovery có budget riêng, không lặp vô hạn. Retry cùng lý do không reset sau mỗi stage.

Ví dụ: capture 1 no-face → capture 2 quality fail → capture 3 S4 unresolved → MANUAL. Không cộng thêm 2 S4 retry và 1 S8 retry. Resume active attempt giữ counters, không reset bằng nhập lại cùng SBD hoặc kết nối lại. Thay claimed record phải kết thúc/ghi nhận lượt cũ và tạo lượt mới, không chuyển evidence giữa hai reference.

## 6. AIConfig và audit

AIConfig có version liên kết hash model pack, detector/config, preprocessing, S4 parameters, S8 rule/operating point và quality criterion thực sự được triển khai. Mốc P2/S8 nghiên cứu đọc từ [freeze T-023](../05-evaluation/T-023-evaluation-freeze.md); T-024 **không tự khóa ngưỡng triển khai** hoặc đổi tín hiệu reused cosine thành một verifier độc lập.

Mỗi observation ghi attempt ID, chỉ số capture, lý do/retry counters, S4 outcome/selected box, reference mapping version, S8 outcome/score và version AIConfig. Bằng chứng ảnh/embedding nếu lưu phải theo quyền/retention, ngoài Git; không yêu cầu thu mọi dữ liệu chỉ để “có audit”.

Trước demo test cần chốt capability quality nào thực sự có, người nhận manual, budget được duyệt và cách đo attempt-level risk/runtime. Policy retry mới chưa có kết quả chạy; không suy từ T-023 rằng retry sẽ tăng độ chính xác hay giảm false acceptance.
