# BUM tiền đạo 07: giai đoạn 1

**Art gate: chưa đạt. Không có phê duyệt 9/10, không nhân rộng ba nhân vật còn lại.**

Yêu cầu đã đổi: Snow không phù hợp danh tính/tuổi BUM và chỉ được giữ để đối chiếu kỹ thuật. Bản C là mesh Blender mới hoàn toàn trong dự án, không có geometry/texture/rig/animation Snow. Không đổi màu hoặc thu nhỏ Snow. Tính năng A/B được mở rộng thành A/B/C; A và B vẫn giữ nguyên. Bản C chỉ áp dụng `bum-player`; chọn BA hoặc BUM thủ môn trở về A. Request C đến muộn phải nhường lựa chọn mới hơn.

## Phần kỹ thuật có thật

Nguồn editable `graphics/models/bum07/bum07-source.blend` và script `scripts/assets/build-bum07.py`. GLB nhúng `bum07-study-portrait.glb` và `bum07-study-mobile.glb` có 4 clip Idle/Run/Kick/Celebrate thật, 51 khớp, skin weights. Chuyển động là keyframe FK tạo bằng script, chưa phải motion thể thao tự nhiên, chưa có facial/IK/corrective rig hoàn chỉnh. Save bị khóa vì không thuộc phạm vi tiền đạo.

Head là surface field mới định hình vùng mũi/má/cằm; body/hand là volume hợp nhất; hair là shell có rãnh chải, không dùng tube locks của bản cũ. Jersey vàng, 07 tự dựng vector, badge mặt trời riêng, quần navy, tất và boot/studs/laces. **Các yếu tố này vẫn là nghiên cứu bằng script, chưa phải chất lượng sculpt/phục trang chuyên nghiệp.**

Bản C được ghi rõ “chưa duyệt” trong giao diện và PNG xuất. Không tự gọi mô hình là điện ảnh/premium chỉ vì dùng Blender hoặc GLB.

## Vì sao chưa thể nghiệm thu 9/10

Render thật còn lộ kiểu tóc giống vỏ/mũ, mắt/mí và đường miệng thiếu tinh tế, garment pattern và nếp vải chưa thuyết phục, chuyển tiếp khớp/bàn tay cần retopo và cleanup. Rig hiện chưa có IK/contact, chân trụ/tiếp xúc bóng và facial performance cần làm tay. Tăng polygon hoặc đổi tên shader không thay thế được các bước này.

Phương án sản xuất cụ thể bằng Blender, vẫn ưu tiên công cụ/nguồn miễn phí: [hồ sơ tạo hình, sculpt, retopo, hair/cloth, UV/PBR, rig/animation và nghiệm thu](../graphics/models/bum07/PRODUCTION-BRIEF.md). Cần công việc sculpt/animation có phán đoán mỹ thuật của họa sĩ; môi trường hiện chạy được Blender/export/test, nhưng kết quả tự động hiện tại chưa đạt chất lượng người dùng yêu cầu. Không mua/thuê ai.

## Ngân sách thực tế và kiểm chứng

- Portrait: 160,634 tam giác mesh, 6,443,416 bytes.
- Mobile: 104,951 tam giác, 4,322,496 bytes; vùng mặt được giữ nhiều geometry hơn phần thân.
- Gộp geometry theo 15 vật liệu: studio quan sát 18 draw calls. Một normal tile nhúng 128², ước tính texture RGBA8+mipmap 0.08 MiB; chưa phải bộ texture PBR đầy đủ đạt yêu cầu cuối. Không dùng số ít texture làm bằng chứng chất lượng cao.
- Chỉ cache một candidate LOD trên GPU; không tự giảm DPR/chất lượng. Decoder texture KTX2 và iPhone vật lý chưa kiểm chứng.
- GLB timeline đọc đúng duration mỗi clip, `seek` loại bỏ fade đang dở khi scrub; không dùng time procedurally giả làm clip GLB.
- `tests/bum07.cjs`: A/B/C, 4 clip, pixel deformation, LOD, ảnh face/full/profile/back, mobile layout, ràng buộc chỉ BUM striker, request đến muộn và zero Supabase.

Ảnh/video/báo cáo đặt ở `showcase/bum07-review/`; chúng là render thật từ GLB, không phải ảnh concept AI. FPS chỉ có giá trị trong môi trường đo, không dùng giả lập Linux để cam kết Safari iPhone mượt.

Game index/scene, bốn mô hình A, Snow B, dữ liệu/quyền Supabase và game GitHub Pages không thay đổi. PR #2 không merge; trước khi nhân rộng phải có chủ dự án duyệt BUM 07.
