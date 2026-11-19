# P5.3A — Checklist nghiệm thu

PASS kỹ thuật không phải phê duyệt mỹ thuật. Chủ dự án đã cho phép dựng blockout; chưa cho phép P5.3B.

| Tiêu chí | Trạng thái | Bằng chứng / giới hạn |
|---|---|---|
| File .blend đọc lại được, mesh sửa được | PASS_NATIVE | audit-blockout.py mở lại file; các object/mesh/camera trong file |
| Tạo mới mặt, không lấy Scott | PASS_SOURCE | build-blockout.py không import asset/mesh; lịch sử P4 không đổi |
| Tỷ lệ mục tiêu5H | PASS_BLOCKOUT | bbox skull–floor/H≈5.0007; không phải đo từ ảnh AI |
| Một model cho mọi góc | PASS_STATIC | fingerprint mesh/transform/material và lights trước/sau render |
| Camera orthographic thật | PASS_PROJECTION | CameraData ORTHO; đoạn1H ở hai độ sâu có cùng độ phóng đại |
| Số07 không kéo giãn | PASS_BOUNDS | cao trước0.38H/sau0.42H, trong dung sai0.005H |
| Số áo bám mặt vải | PASS_GEOMETRY | mọi vertex cách shirt evaluated dưới0.003H |
| Không lộ sclera bất thường0/45/90 | PASS_SAMPLED_STATIC | ray grid được ghi rõ; cần đọc thêm PNG. Không chứng minh từng pixel/mọi góc liên tục |
| Không ẩn mesh/đổi mesh theo camera | PASS_STATIC | hidden-character-list rỗng, không animation/actions/shape keys |
| Cung tám răng trên duy nhất | PASS_STRUCTURE | một object, tám thành phần; chưa rig hoặc kiểm khớp cắn |
| CổV trước, bo sau; kit vàng/navy/07 | REVIEW_2D | xem PNG0/45/90/180; geometry đo camera riêng; không phải mô phỏng pattern may |
| Render0/45/90/180, A-pose, face0/45 và face90 bổ sung | PASS_FILES khi inventory/checksum đạt | 7 render độc lập1200×1600 +1alias A-pose có công bố |
| Chất tóc tự nhiên như conceptB | FAIL_ART_FINISH | còn khối/rãnh cứng, không phải tóc sculpt cuối |
| Mặt/mắt/môi đạt độ duyên và sinh động conceptB | FAIL_ART_FINISH / OWNER_REVIEW | gaze, khóe mí/môi, tai/cằm còn đơn giản; mắt45° có cảm giác lồi và catchlight quá rộng; không tự đánh giá9/10 |
| Kit/tay/giày chất lượng production | FAIL_PRODUCTION | blockout; mép cổ/piping/gấu/dải tất còn không đều; chưa hoàn thiện vải, bàn tay và giày |
| Topology/UV/rig/skin/biểu cảm/GLB | NOT_TESTED | ngoài P5.3A; không có rig/animation/GLB sản xuất |
| Hiệu năng Safari/iPhone | NOT_TESTED | không tích hợp game hoặc đo FPS |
| main/Pages/PR2/historical files nguyên vẹn | PASS_SCOPE khi protection-check xác nhận | so tên file thay đổi và SHA đọc từ GitHub |
| Supabase | NO_ACCESS | không request hoặc sửa Supabase |
| Được phép P5.3B | CLOSED | dừng chờ chủ dự án duyệt ngoại hình |

Lỗi/giới hạn còn tồn tại phải đọc cùng TECHNICAL-AND-ART-REPORT.md, không dùng việc archive/export thành công để thay nghiệm thu mỹ thuật.
