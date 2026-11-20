# P5.4 — Checklist nghiên cứu và tiêu chí nghiệm thu tương lai

## Kết quả có thể xác nhận trong P5.4

| Yêu cầu | Trạng thái | Bằng chứng / giới hạn |
|---|---|---|
| Nhánh riêng từ928d212 | PASS khi commit/push | Git parent; chỉ thêm thư mục P5.4 |
| Đánh giá R/B1 không tạo khuôn mặt procedural mới | PASS | Audit chỉ đọc; source SHA trước/sau bằng nhau; không gọi save/export/sculpt |
| Có hai hướng và so rủi ro/công việc | PASS tài liệu | COMPARISON; cả hai cần sculpt bằng tay, không hứa9/10 |
| Khảo sát asset có nguồn/license cụ thể | PASS theo phạm vi |5ứng viên; Tiby + Human bundle mở native, còn3binary chưa mở |
| Head Generic quyền sử dụng | PASS phạm vi đúng asset CC0 | Metadata object + README; giữ Rain notice riêng, không ápCC0 cho Rain Rig/code |
| License mọi thành phần của binary chưa tải | CHƯA KIỂM CHỨNG | Boy/Spring/Quaternius cần kiểm file khi được chọn; không tự gọi production-cleared |
| Đối chiếu từng asset với5H/oval/mắt/mũi/môi/tóc | PASS nghiên cứu | ASSETS-LICENSES; chưa đo5H/khớp mỹ thuật donor, nêu rõ unknown |
| Rig/deformation/GLB/iPhone thực nghiệm | NOT_RUN / ngoài phạm vi | Native rig counts chỉ là cấu trúc; không biến thành kết quả export/playback |
| Checkpoint silhouette/face/hair/expression/body riêng | PASS kế hoạch | ARTIST-WORKFLOW G1..G5 có cổng chủ dự án duyệt |
| Mua/thuê/sculpt sản xuất/đổi model game | KHÔNG THỰC HIỆN | Native mới tải chỉ ở/tmp; không BUM adaptation hoặc model mới |
| main/Pages/PR2/Supabase/3nhân vật/lịch sử | Giữ nguyên theo kiểm tra bảo vệ | Snapshot readonly và diff;0request Supabase, không merge |
| Chủ dự án chọn A/B, nghiệm thu mỹ thuật | PENDING | Không tự chọn thay chủ dự án; dừng sau báo cáo |

## Ma trận PASS/FAIL cho quá trình tương lai — chưa phải kết quả P5.4

| Cổng | Bằng chứng bắt buộc | PASS đề xuất | FAIL phải dừng |
|---|---|---|---|
| G1 Silhouette | Native1model; ORTHO0/45/90/180; clay + thướcH | Oval/profile trẻ em đúng B, chủ dự án duyệt | Mấu cằm, hộp sọ/neck lệch, chỉ đẹp1góc; camera che lỗi |
| G2 Face | Face0/45/90; clay và vật liệu cơ bản, report landmark | Mắt hạnh nhân, mí/khóe/mũi/môi/má mềm, ánh nhìn tự nhiên, được duyệt | Mắt lồi/vô hồn, flat smile, hàm người lớn/plastic, chệch B |
| G3 Hair |0/45/90/180 + góc cao, hairline/part/gáy | Rẽ trái giải phẫu, mái thấp, cụm mềm có chiều sâu, được duyệt | Mũ/ống nhựa/rãnh đều, part sai/mirror, tóc gáy hở bất hợp lý |
| G4 Expression |8trạng thái×front/45; Blink5mức; Smile3mức + phối hợp | Giữ identity/volume/teeth, blink kín bằng mí thật; chủ dự án duyệt | Bất kỳ lộ iris/sclera bất thường ởBlink100; đổi người/răng/cung, xuyên/flat seam |
| G5 Body | Fullbody4góc+A-pose, số đo5H, kit07, hands/boots | Đúng palette/tỷ lệ, năm ngón, kit và số07 rõ, được duyệt | Scale camera giả5H, sponsor ngoài thiết kế, số giãn/xuyên, body trưởng thành |
| G6 kỹ thuật | Actual native/GLB comparison, deformation/browser/thiết bị | Các bài đo thực đạt ngưỡng đã duyệt và ảnh giữ chất lượng | Chưa chạy mà PASS; xóa bones/cắt influences làm hỏng deform; dùng desktopWebKit làmFPSiPhone |

Cổng mỹ thuật do chủ dự án duyệt rõ ràng. Manifold, file mở được, license hợp lệ, polycount nhỏ hoặc export thành công không thay được nghiệm thu mỹ thuật. Nếu thay đổi phá checkpoint trước thì quay lại duyệt đúng phần đó. Không tiếp tục vòng tham số vô hạn, không tự mở giai đoạn mới.
