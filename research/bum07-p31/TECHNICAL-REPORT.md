# Báo cáo P3.1 — tách kết quả dữ liệu khỏi nghiệm thu mỹ thuật

## Kết luận

**FAIL_ART_TARGET / FAIL_FACIAL_DEFORMATION.** P3.1 là thử nghiệm procedural mới, có lợi ích cục bộ nhưng chưa tạo cải thiện mỹ thuật đủ đáng kể để nghiệm thu; chưa đạt 9/10. Body và rig gốc giữ nguyên, lỗi áo/clip C không thuộc phạm vi sửa lần này. Không chuyển P3.2.

## Kiểm tra và giới hạn

| Hạng mục | Kết quả kiểm chứng | Giới hạn |
| --- | --- | --- |
| Nguồn | P2 SHA-256 giữ nguyên; file mới riêng | Không ghi đè C/P2 |
| Read-back Blender | 95 mesh gốc, rig/rest matrices/action curves giữ nguyên | 95 gồm reference/P2; 44 mesh body/outfit ngoài phạm vi |
| Mesh mới | 27 component; boundary=0, non-manifold=0, inconsistent winding=0, degenerate faces=0; signed volume dương | Kín từng component; không phải head/lids welded, không chứng nhận inter-object intersections |
| UV | Các mesh mới có UV hữu hạn, GLB có TEXCOORD_0 | UV tham số, chưa chứng nhận overlap/distortion/bake layout; torso C cũ không có UV, không sửa |
| GLB | 225.446 tam giác tổng, 71 primitives; buffer/texture nhúng, normals mới unit, skin weights hợp lệ, mọi accessor hữu hạn, morph sparse đọc được | Audit riêng của dự án, không gọi là Khronos certification. Budget này chưa chốt cho iPhone |
| Morph data | Blink/Smile ở 0/50/100% hữu hạn; không tam giác diện tích 0 trong bài đọc lại | Không suy ra không xuyên mesh; ảnh Blink 100% **FAIL**, còn lộ iris/sclera |
| Head skin/action | Idle/Run/Kick/Celebrate ở đầu/giữa/cuối clip: evaluated geometry hữu hạn, head thật sự theo rig | Chỉ skin Head và facial study, chưa rig mặt production; chưa animation cleanup/collision solver |
| Chromium/WebKit | Xem `renders/*/browser-report.json`: real GLB import/render, 12 matched views, expression/motion, 390×844 layout, zero page errors/Supabase requests khi PASS | Browser PASS chỉ nói luồng test chạy được; không phải mỹ thuật đạt. WebKit WPE Linux không phải Safari iPhone |
| iPhone | Chưa kiểm thử thiết bị thật | Không công bố FPS/độ mượt iPhone từ máy Linux |

## Giao thức ảnh

C/P2/P3.1 cùng studio Three.js hiện có, 35° vertical FOV, viewport 1500×1100 DPR1. Canvas thực ghi riêng theo engine trong report (Chromium 1180×866, WebKit 1180×857 do layout/font). So sánh ba variant trong cùng engine; không so pixel giữa hai engine. Bốn góc: chính diện, 45°, profile 90°, close thêm cùng một bước zoom. Mỗi variant cùng neutral Idle time0, model normalization height2,2 của importer review; camera/target/angle khóa theo C, sai số camera/target <1e-6. Không đổi lens/light/grading hoặc rescale từng ảnh để giấu lỗi. Bảng ghép chỉ đặt PNG nguyên kích thước cạnh nhau và thêm nhãn.

C/P2 ở đây được render lại từ GLB gốc, không sửa geometry; P2 GLB sha `6121dbdd994b030318291c24a813d007960d767c54e1d101f54ff28099ee5a3c`. Ảnh gốc của hồ sơ vẫn ở `docs/artist-production/BUM07/BASELINE-P2`; camera P2 trước kia follow head riêng, nên hash PNG P2 không cần giống ảnh render lại với matched-camera theo C.

## So sánh quan sát

| Vùng | C/P2 | P3.1 | Trạng thái |
| --- | --- | --- | --- |
| Mắt | Globe nhô, mí patch; P2 eye silhouette lệch | Globe lùi, socket field mới nhưng còn sclera ở mép trên, vành mí lộ | Chưa đạt |
| Mũi/má | Chuyển tiếp chưa mềm và thiếu cá tính | Surface liên tục mới nhưng mũi và shadow vẫn thô, má thiếu biểu cảm | Chưa đạt |
| Miệng | Cười dạng đường, lip seam | Lip volume kín mới nhưng vẫn mảnh/phẳng, smile không phối hợp đủ | Chưa đạt |
| Tóc | C cap; P2 dải răng cưa và nổi | 8 leaf volumes bám scalp, ít vỡ hơn; base cap và các khối đều còn rõ | Cải thiện cục bộ, chưa đạt |
| Facial deformation | Study chưa production | Blink xuyên iris/sclera; finite data không giải quyết collision | FAIL |

## Nguyên nhân và chặn nghiệm thu

Các analytic fields riêng cho hốc mắt, mí, globe và leaf projections chưa hình thành anatomical surface thống nhất. Chưa có eyelid contact/corrective solver, welded deformation loops và art-directed silhouette. Nhiều samples/manifold/closed volume không thay được chất lượng thiết kế form. Không thể gọi là sculpt chuyên nghiệp hoặc đạt 9/10.

Các hướng cần đánh giá **chỉ sau phản hồi P3.1**: topology mí–socket liên tục và corrective dựa globe, thiết kế lại silhouette/roots/hair masses thay vì phủ nền cap, phối hợp môi–má–brow có kiểm tra ảnh. Đây là ghi nhận tồn đọng, không phải tự khởi động P3.2 hoặc thuê artist.

GPU/user-agent strings trong report chỉ là thông tin browser công bố (WebKit có thể trả Apple GPU ngay trên Linux WPE); không phải chứng cứ phần cứng Apple/iPhone. Không dùng các chuỗi này suy ra thiết bị thật.
