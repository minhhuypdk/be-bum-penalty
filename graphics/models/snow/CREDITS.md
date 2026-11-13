# Snow asset nền — không phải BA/BUM hoàn thiện

**Snow Rig © Blender Foundation | studio.blender.org**

Nguồn chính thức: https://studio.blender.org/characters/snow/v3/

Giấy phép **Creative Commons Attribution 4.0 International (CC-BY 4.0)**:
https://creativecommons.org/licenses/by/4.0/

Được phép sử dụng, sửa và phân phối, bao gồm thương mại, với ghi công, liên kết giấy phép và nêu thay đổi. Không có xác nhận hoặc bảo trợ của Blender Foundation cho dự án này.

## Thay đổi trong bản duyệt

Đánh giá mesh từ pose nguồn; thay shader Cycles bằng PBR dựa trên texture gốc; nhúng texture JPEG (albedo mặt/tóc/mắt tối đa 2K, áo/quần/da thân tối đa 1K; normal/roughness có ngân sách riêng); giảm subdivision/texture cho mức Mobile; chỉ giữ khớp có trọng số và bind pose. Dựng lại chuỗi khớp chính, tư thế đứng hạ tay; thêm clip Idle quay đầu rất nhẹ để kiểm tra skinning. Không mang theo mã CloudRig, driver hoặc script tự chạy của file Blender.

## Giới hạn cần nghiệm thu

Đây là mô hình nền để kiểm tra pipeline và so sánh tạo hình, không phải BA/BUM, không phải bốn nhân vật hoàn thiện và chưa được đánh giá đạt 9/10. Trang phục gốc chưa phải áo đấu hoặc găng thủ môn. Rig review không thay thế rig diễn xuất gốc; chưa có blink, biểu cảm khuôn mặt, chạy, sút, bay bắt bóng hoặc ăn mừng đạt chất lượng cuối. Các clip thiếu bị vô hiệu hóa. Chưa có số đo trên iPhone thật.

Manifest ghi SHA-256 nguồn và thay đổi. Script xuất tái lập nằm tại scripts/assets/export-snow.py trong repository. Không đưa nguyên file Blender 107 MB vào bản tải trình duyệt.
