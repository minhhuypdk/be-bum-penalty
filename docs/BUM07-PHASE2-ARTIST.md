# BUM 07 Phase 2 — mặt/tóc, chưa nghiệm thu
Không có xác nhận 9/10. Đây là mesh-edit/blockout tính toán, không phải sculpt thủ công chuyên nghiệp. Blender/export hoạt động; giới hạn là chất lượng tạo hình, anatomy và retopology của phương pháp tự động.

## Phân tích sáu ảnh C
- Chính diện/cận mặt: mắt như dán lên mặt, mí yếu, mũi nhô, nụ cười như nét vẽ, brow/cheeks còn đơn giản.
- 45°/nghiêng: globe nhô trước silhouette, chuyển plane nose/lip chưa tự nhiên.
- Sau lưng: tóc là vỏ có rãnh, thiếu layer/roots có chiều sâu.
- Pose sút: áo kéo gãy/thủng là lỗi ngoài Phase 2; chỉ ghi nhận, chưa sửa body/rig/animation.

## Trong file bum07-facehair-workbench.blend
- 00_C_LOCKED_FACE_REFERENCE: mặt/tóc C ẩn, khóa chọn, giữ nguyên để so sánh.
- 01_P2_FACE_HAIR_EDIT: head/socket/lids/eyes/brows/lips và khối tóc được phép chỉnh.
- 02_P2_HAIR_RAW_GUIDES: scalp cùng 10 guide cụm tóc ẩn; bật khi bố trí lại khối/hướng.
- 03_C_BODY_OUTFIT_LOCKED: 44 mesh thân/trang phục không được sửa giai đoạn này.
- Sáu ảnh C_REFERENCE_approval-*.png đã packed, fake-user; chọn trong Image Editor không cần đường dẫn máy tạo.
- ART_Front / ART_45 / ART_Profile hỗ trợ artist; so sánh thực tế dùng cùng studio Three.js 35° cho C và P2.
- Text READ_ME_PHASE2_ARTIST.txt nhắc phạm vi. Vật liệu P2 được sao chép riêng.
- FH_Blink/FH_Smile chỉ là shape studies tĩnh; chưa là facial performance hoàn thiện.

## Mesh edits thực tế trong nghiên cứu
Giảm projection mũi, chỉnh nhẹ vùng cằm; tạo opening quanh mắt, annulus mí có relief và globe nhỏ đặt sâu hơn; môi nhỏ có độ nổi thay nét cười cũ. Tóc dùng 10 guide khối riêng rồi hợp nhất giao cắt thành nền sculpt; không chỉ tăng subdivision cap C.
Các seams/lid anatomy, lip transition và hair silhouette vẫn cần artist xử lý. Nhiều polygon hoặc GLB hợp lệ không chứng minh chất lượng điện ảnh.

## Artist Blender làm thủ công
1. Save As bum07-facehair-artist-v001.blend. Không overwrite C hoặc bản bàn giao. Giữ C reference/body khóa; chỉ chọn P2.
2. Dùng clay/matcap đọc khối front/45/profile. Không đổi ánh sáng để che lỗi. Chưa đổi cổ/vai/thân, tỷ lệ cả nhân vật hoặc animation.
3. Head đang có shape keys: duplicate thành bản high-poly riêng, chỉ remove keys/remesh/Dyntopo trên bản sao. Không phá vertex order bản keyed.
4. Retopo vòng hốc mắt và annulus mí thành loops tương ứng, bridge/weld đúng topology. Hiện còn seams cần cleanup. Kiểm tra normals/Face Orientation, khóe mắt, mí trên che globe, lower lid mỏng; Blink không được xuyên iris/sclera.
5. Cân iris/pupil và hướng nhìn trẻ em; brow taper mềm bám da. Đừng chỉ phóng mắt to.
6. Sculpt bridge/tip/nostril/philtrum, má và khóe/môi nhỏ có chuyển tiếp. Nét đen hoặc dải môi tô nổi không phải sản phẩm cuối.
7. Tóc: bố trí 3–5 khối chính với khối phụ từ RAW_GUIDES; root tiếp scalp, đầu thuôn, hướng chải nhất quán. Sculpt khối hợp nhất bằng Clay/Crease/Smooth; retopo silhouette và bake detail sau khi duyệt khối lớn. Không giữ vỏ trơn hoặc ống cong làm tóc cuối.
8. Sửa FH_Smile/FH_Blink ở trạng thái tĩnh; phối hợp môi/khóe/má và mí. Neutral ở Basis. Không tạo sports animation ở Phase 2.
9. Làm UV/PBR mặt/tóc sau anatomy; tránh highlight giả vẽ sẵn. Vật liệu áo/quần/giày không đổi.
10. Render front/45/profile/close đặt cạnh C, cùng camera/ánh sáng/neutral. Chỉ chuyển body/animation khi chủ dự án nghiệm thu ảnh.

## Dữ liệu và giới hạn
source-audit.json là kết quả đọc lại C và workbench độc lập: geometry/UV/material/weights ngoài phạm vi, bones/actions, C-head-reference, hair volume và sáu ảnh packed. Không dùng mỗi boolean của builder làm bằng chứng.
GLB giữ bốn action C nguyên bản, không phát triển animation mới. Hair runtime có budget riêng (90k/45k hair triangles), source sculpt không bị giảm theo LOD. Chưa có FPS Safari iPhone thật.
Nguồn/bộ mới không có mesh/texture/rig/animation Snow. A/B/C, PR draft, main/game công khai và Supabase giữ nguyên. Chưa mua hoặc thuê ai.
