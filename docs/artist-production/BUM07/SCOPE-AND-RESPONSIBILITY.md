# Phạm vi và phân công

| Công việc | Codex tự làm được | Cần artist 3D | Quyết định cuối |
| --- | --- | --- | --- |
| Đóng gói file/refs, kiểm hash và khả năng mở | Có; không sửa mesh khi đóng gói | Kiểm lại file có thể chỉnh tay | Chủ dự án nhận hồ sơ |
| Hướng tỷ lệ/landmark | Chuẩn hóa tài liệu thành một master proposal, đo dữ liệu hiện có | Kiểm form và đề xuất chỉnh có căn cứ | Chủ dự án duyệt direction bằng ảnh |
| Sculpt face/hair đẹp, cá tính và anatomy | Không coi mesh script/ảnh AI là sculpt chuyên nghiệp | Artist quyết định khối, silhouette, planes, transition và diễn xuất | Chủ dự án nghiệm thu hình ảnh |
| Retopology/UV/weight paint facial | Kiểm dữ liệu, topology warnings và scope | Artist xây loop, UV, weight và correction có phán đoán mỹ thuật | Artist tự QA; chủ dự án nhìn ảnh |
| Facial rig/expressions | Lập mapping/test GLB và phát hiện lỗi kỹ thuật | Artist tạo Basis, shapes/bones/corrective và cleanup expression | Chủ dự án duyệt neutral/smile/focus/blink |
| Materials/bake | Kiểm color space, file links, size và runtime compatibility | Artist làm texture/bake/lookdev sau clay approval | Chủ dự án duyệt look |
| Export GLB/runtime | Kiểm import/skin/morph/console; cấu hình decoder khi được phép | Artist giữ source và xuất đúng dữ liệu | Codex PASS kỹ thuật không phải 9/10 |
| LOD/FPS iPhone | Đo trên thiết bị thật khi có, báo đúng môi trường và tối ưu kỹ thuật sau art approval | Artist bảo vệ silhouette/morph khi làm LOD | Chủ dự án duyệt trade-off chất lượng |

## Những việc Codex không tự nhận đã làm

Không tạo P3/P4 bằng deform/remesh tự động rồi coi là production. Không tự chấm 9/10, không gọi tăng resolution/đổi HDRI là sculpt, không dùng ảnh concept AI làm render GLB. Không thay mesh của artist để tự diễn giải master mà thiếu bằng chứng hình ảnh. Không mua/thuê hoặc nhắn artist bên ngoài trong phiên này.

## Những phần bị khóa

Chỉ BUM tiền đạo 07, giai đoạn mặt/tóc. Giữ nguồn P2 nguyên byte, A/B/C và body/outfit/animation hiện có. Không phát triển ba nhân vật còn lại. Không merge PR #2, không sửa main/game GitHub Pages, quyền/schema/dữ liệu Supabase. Artist làm trên bản sao có tên làm việc riêng, không ghi đè SOURCE hoặc gọi bản đó là P3/P4 tự động.

## Đầu ra artist phải giao

Editable .blend với high/low và textures packed; GLB thực với skin/morph phù hợp, target mapping; bốn cặp PNG matched-render và ảnh expressions; metadata camera/lighting/source hash; danh sách lỗi đã sửa/còn mở. Nếu có asset ngoài, phải ghi nguồn và quyền dùng/sửa/phân phối GLB trên web/repository. Chưa có giao dịch hoặc nguồn asset ngoài mới trong hồ sơ này.

## Cổng duyệt

1. Hồ sơ/master proposal được xem xét (chưa phải duyệt mô hình).
2. Artist giao clay mặt/tóc front/45/profile; chủ dự án chấp thuận form.
3. Artist hoàn thiện retopo/facial/material và giao bốn ảnh matched-render + expression tĩnh.
4. Codex kiểm file/runtime, chủ dự án duyệt mỹ thuật. Chỉ sau đó mới mở giai đoạn body/animation.

Mọi checklist art mặc định OPEN. VALIDATION.json của gói chỉ xác nhận file/tài liệu, không đổi các gate trên thành PASS.
