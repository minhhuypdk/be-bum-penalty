# Quy trình sculpt thủ công đề xuất — chưa thực hiện

Đây là phương án giải quyết giới hạn đã quan sát, không phải cam kết có model đẹp hơn hoặc yêu cầu thuê artist ngay. Chỉ triển khai sau khi chủ dự án xem P5.3B.1 và phê duyệt bước tiếp theo.

## File đầu vào và vùng được phép

Mở `bum07-p53b1-head-study.blend`, Save As file mới ngoài bản đã bàn giao. Giữ `reference/bum07-p53ar-preserved.blend` làm đối chứng; không ghi đè C/P2/P3/P4/P5 hoặc native B1. Chỉ sửa các mesh B1 head/hair/ear và tiếp giáp cổ cần đánh giá; không outfit/tay/chân/rig. Đầu giữ datum Z4..5 =1H; tỷ lệ mục tiêu5H vẫn là hướng thiết kế, không đo toàn thân mới.

## 1. Layout và silhouette trước chi tiết

Đặt ảnh concept B và P5.2R trong Image Editor bên cạnh viewport; ghi rõ ảnh AI có bất nhất, không chiếu mù lên mesh. Khóa camera0/45/90/180 và đèn studio. Dùng MatCap đơn sắc để nhìn khối, rồi quay lại vật liệu cuối để kiểm tra.

Trên bản sao đầu, dùng Grab/Elastic Deform cỡ lớn để giảm mấu cằm ở profile, làm oval má–hàm và đường trán–mũi mượt. Không dùng Smooth toàn đầu làm mất mí/môi. Chốt silhouette cả front và profile trước khi tăng detail; lưu checkpoint riêng. Hạn chế symmetry tuyệt đối ở mức biểu cảm nhưng không làm lệch hộp sọ.

## 2. Khối mặt

Dùng Clay Strips/Clay Thumb nhẹ cho bọng má và muzzle, Scrape/Fill để chuyển mặt phẳng trán–thái dương. Mũi trẻ em: bridge thấp, tip mềm, cánh mũi có độ dày thay vì một Gaussian nhô. Kiểm tra dưới ánh sáng phẳng và ánh sáng studio, không dùng SSS che thiếu volume. Môi trên/dưới có pillows, khóe cắm vào má và nhân trung vừa đủ; không chỉ thêm đường seam nổi.

## 3. Orbital, mí và ánh nhìn

Giữ globe hình cầu làm thước tham chiếu khi sculpt. Có thể Mask globe trong thao tác sculpt, nhưng **không tắt render/ẩn để bàn giao**. Grab/Clay tạo khối hốc trên/dưới ôm globe; mí trên chồng hợp lý lên mí dưới ở canthus, có thickness thật. Mí dưới ôm nhãn cầu thay vì rãnh lớn. Gaze cần đồng hướng hội tụ xa, iris/pupil gắn theo phép quay quanh tâm; không dịch cap xuyên globe. Sau chỉnh, đo radial clearance và kiểm tra front/45/90. Chưa tạo Blink hoặc facial rig trong phạm vi này.

## 4. Tai/cổ

Sculpt helix/antihelix thành relief mềm, concha có lõm vừa phải, lobe đầy; tránh vòng dây nổi. Kiểm tra projection chiều sâu ở45/90. Đầu–cổ chỉ cần chuyển khối tự nhiên trong bust; chưa gọi là nối topology deform-ready. Không tăng độ trưởng thành bằng hàm góc hoặc cổ dày.

## 5. Tóc

Trên bản sao tóc, giữ hairline rẽ trái và mái thấp của B. Dùng Grab/Clay/Scrape để chia 3–5 khối chính có hướng mọc; phá độ tròn đều của cap bằng chênh cao/thấp và vài khoảng âm vừa phải ở silhouette. Cụm mái cần chân xuất phát từ part, đi qua trán rồi taper, không là những tấm dán. Mái/nape không cùng độ dày; kiểm tra cả sau180 để tránh hairline dạng vòng ngang.

Voxel remesh chỉ khi cần union lại; chọn voxel theo form cần giữ, không thêm polygon để thay sculpt. Sau remesh kiểm tra mất bờ mí/miệng nếu dùng trên đầu. Chỉ thêm rãnh phụ nhỏ khi khối chính đã được duyệt; không quay lại các rãnh dài song song.

## 6. Cổng kiểm tra trước khi xin duyệt

Render cùng camera/ánh sáng, không beautify hậu kỳ. So cạnh concept B, R và B1; đánh dấu rõ những điểm chệch. Kiểm tra profile cằm, khoảng trắng mắt, khóe môi và silhouette tóc trước khi xin duyệt. Nếu không tốt hơn ở cả0/45/90, không chuyển sang rig hoặc “production”.

## Phân công thực tế

| Codex tự làm được trong môi trường hiện tại | Cần thao tác sculpt có phán đoán mỹ thuật / người dùng Blender |
|---|---|
| Script scene, reference layout, datum, camera/đèn; lưu native và version | Quyết định và kéo khối oval/head silhouette đẹp ở nhiều góc |
| Mesh generation/remesh, audit finite/manifold/clearance, render lặp cùng setup | Dùng brush và tablet/mouse để sculpt mí, khóe, môi, má, tai tinh tế |
| Đóng gói PDF/checksum, so trước/sau, báo lỗi cụ thể | Thiết kế khối tóc/hairline bất đối xứng mềm, giữ nhận diện B |
| Ghi nhận giới hạn và dừng khi procedural chưa đạt | Đánh giá nghệ thuật và điều chỉnh form dựa trên render thực |

Chưa thực hiện thao tác thủ công trên file này. Không giả nhận có artist tham gia hoặc có sculpt bằng tay. Chưa cần quyết định rig/retopo/animation/GLB cho đến khi khuôn mặt và tóc được duyệt rõ ràng.
