# BUM07 P5.2R — So sánh thiết kế và giới hạn

Baseline `8529f6b`, nhánh `research/p52r-bum07-design-lock`. Ngày 18/11/2026.
**OWNER_PENDING; Blender gate CLOSED.** Không tự công bố đạt 9/10.

## Trước / sau

| Hạng mục | P5.2 | P5.2R | Bằng chứng / giới hạn |
|---|---|---|---|
| Hairline, ngôi | Các góc có độ phồng/đường tóc khác nhau | Giữ front làm master; giảm phồng 45°, làm mềm thái dương/profile; ngôi trái giải phẫu | PDF turnaround trang 2–5; continuity quanh đầu chưa chứng minh |
| Gáy | Mép nhọn dễ thành chữ V | Mép mềm, rộng hơn, taper thấp trên cổ navy | Không tuyên bố dịch chuyển chính xác theo pixel hoặc đo độ cao 3D |
| Tai/má/mũi/cằm | Chuyển góc chưa đồng nhất | Tai gần đầu hơn, đầu mũi/cằm mềm ở45/90°, giữ nét trẻ em | Quan sát 2D; chiều sâu chính xác NOT_VERIFIED |
| Focused | Mày chụm, vẻ nghiêm/giận | Giảm chụm mày, mắt mở, môi tự tin nhẹ | So sánh cả0/45 trong PDF biểu cảm; sắc thái chờ chủ dự án duyệt |
| Celebration | Nheo mắt mạnh | Mở mắt để thấy iris, cười reo | Đã thấy trong ảnh; không đo % mở mí từ mesh |
| Răng | Kích thước/cung trôi | Một mẫu SVG tám răng trên, không khe chủ ý; dùng làm tham chiếu chung | **FAIL khóa răng tuyệt đối:** ảnh Smile/Celebration vẫn khác độ rộng/số răng lộ; chưa chứng minh cùng cung 3D |
| Áo trước | V và piping có biến thiên | Giữ V nông, đường raglan; fullbody07 vẫn rõ | Nếp vải/cổ trong portrait vẫn thay đổi nhẹ; không phải pattern may đã dựng |
| Áo sau | Cổ sau và gáy cần chốt | Cổ navy bo liên tục, BUM/07 rõ, không sponsor | Quan sát ảnh180°; chưa có mesh |
| Tỷ lệ, màu | Bảng đề xuất5H | **Không đổi** | Bốn JSON/CSV so byte-identical; không phải số đo mesh |

## Phạm vi ảnh

22 PNG riêng 1024×1536: 15 chỉnh, 7 giữ nguyên có chủ ý. Xem `image-provenance.json` cho SHA256 trước/sau từng ảnh. Giữ front, A-pose và neutral-front làm neo nhận diện; không tạo lại chỉ để đổi nhãn. Nhãn P5.2 trên ảnh giữ nguyên là đúng nguồn.

Ảnh AI là concept, không phải render Blender. 45° mới có crop hơi cao/chặt hơn bản trước; không gọi đây là camera orthographic3D chính xác hoặc cùng camera từng pixel. Bố cục lưới 5H là mốc thiết kế đề xuất, không ép ảnh tự khớp con số. Không sửa palette để khớp màu do ánh sáng của AI.

## Quy tắc thiết kế đề xuất được đóng gói

- Ngôi trái của nhân vật: bên phải người xem ở front, bên trái người xem ở back. Mái thấp quét qua trán; 5–7 nhóm tóc rộng mềm, không quiff cao, không vòng tóc C hoặc tóc Scott.
- Gáy ngắn, mép U/taper mềm; tránh nhọn hình V hoặc chạm/che cổ bo navy. Độ sâu tai và chẩm cần kiểm tra khi có mesh được cho phép.
- Một cung răng trên: UR4→UR1→UL1→UL4; hai răng giữa tròn rộng vừa, răng bên nhỏ hơn, nanh mềm không nhọn. Ở45°, răng xa có thể bị che; không buộc nhìn đủ tám chiếc. SVG là sơ đồ mặt trước, không phải cung đo từ mesh.
- Trước cổ V navy, sau cổ bo navy; piping raglan đi từ cổ xuống nách, 07 trung tâm thân trước/sau, BUM sau trên07; không logo tài trợ. Nếp vải mảnh theo lực vai/nách/hông, không thêm trang trí ngẫu nhiên.
- Mốc và vật liệu đọc từ `specification/` P5.2 giữ nguyên. H tính sọ–cằm không tóc, cơ thể5H, max tóc5.2H. Không thay tỷ lệ để che sai khác góc AI.

## Điều còn phải xử lý trước khi gọi là khóa tuyệt đối

Răng, hairline dưới từng góc, nếp vải và crop chưa khớp tuyệt đối. Không đánh dấu PASS toàn bộ. Chủ dự án cần xem ảnh và chọn có chấp nhận các sai khác minh họa này làm tài liệu dựng hay yêu cầu sửa tiếp. Chưa được phép Blender; không tự chuyển giai đoạn.

Không đo topology/UV/rig/deformation/collision/GLB/FPS ở P5.2R vì chưa có mesh và không được tạo mesh. Không mượn kết quả P4.1R cho bản này.
