# BUM 07 — bộ ảnh mốc trước thay đổi lớn

Bản C giữ trạng thái nghiên cứu, chưa nghiệm thu mỹ thuật và chưa xác nhận 9/10. Chỉ BUM tiền đạo 07 được phát triển; không nhân rộng BA/BUM thủ môn. Không dùng mesh, texture, rig hoặc animation Snow làm BUM.

## Sáu ảnh render thật

Chính diện 0°, góc 45°, nghiêng 90°, sau lưng 180°, cận mặt và pose Kick tại 62% clip ở góc 45°. Cùng GLB, LOD Portrait, ánh sáng studio và camera phối cảnh 35°. Không sửa mesh/texture/rig/animation khi xuất ảnh. Manifest ghi SHA-256 của GLB, nguồn Blender, runtime và từng PNG. Đã xuất/test sáu ảnh tại workspace trước khi môi trường mất kết nối.

Để bàn giao ảnh khi môi trường Codex unavailable, workflow BUM07 frozen render review xuất lại trên nhánh graphics/cinematic-pass và lưu artifact bum07-C-six-renders. Chỉ báo có artifact sau khi run thực tế thành công. Workflow chỉ có contents: read, không sử dụng secrets/Supabase hoặc deploy GitHub Pages. Không merge PR #2.

## Phân biệt phần kỹ thuật và chất lượng mỹ thuật

Đã có: nguồn Blender/GLB độc lập, skin FK 51 khớp, hai LOD, bốn clip nghiên cứu Idle/Run/Kick/Celebrate và A/B/C chỉ cho tiền đạo BUM. Targeted tests trên Chromium/WebKit đã PASS. Kiểm thử đầy đủ bị gián đoạn khi máy Codex unavailable; không gán kết quả PASS cho lượt chưa nhận exit status. Chưa đo trên iPhone vật lý.

Chưa hoàn thiện: anatomy mắt/mí/miệng, tóc vẫn dạng vỏ/mũ, tỷ lệ/chuyển tiếp cổ vai tay chân, bàn tay, nếp vải và PBR cuối, rig facial/IK/correctives, foot/ball contact và diễn xuất tự nhiên. Chưa có clip Jump.

## Lỗi quan sát trực tiếp

- FACE-01: mắt nổi ở góc nghiêng, mí/khóe mắt và nét miệng còn thô.
- HAIR-01: tóc dạng shell, chưa có các cụm sculpt sâu và chân tóc tự nhiên.
- KIT-01: pose Kick lộ áo bị kéo gãy/thủng ở vùng thân/sườn; cần kiểm tra topology, weight paint và corrective, không khẳng định nguyên nhân chỉ từ screenshot.
- HAND-01: hình thể cẳng tay/cổ tay/bàn tay chưa chuyển tiếp tự nhiên; ngón và webbing cần retopo/weight cleanup.
- SHOE-01: upper/đế và fit giày cần kiểm tra geometry/binding/foot roll khi nâng chân.
- MOTION-01: FK chỉ là nghiên cứu; cần cleanup chân trụ, hông, tiếp xúc bóng và follow-through.
- JUMP-01: chưa có clip nên chưa kiểm chứng biến dạng nhảy/landing.

## Artist Blender cần làm thủ công

1. Sculpt mặt trẻ em, hốc mắt/mí/môi/má và cụm tóc có silhouette/chiều sâu riêng.
2. Retopo vòng mắt/miệng/cổ/khớp/ngón, garment pattern và bake texture PBR đúng UV.
3. Facial shapes, IK/pole controls, foot roll, twist/corrective joints; weight paint dưới pose stress test.
4. Animation cleanup cho chạy/penalty/nhảy/ăn mừng; render và nghiệm thu trước khi làm ba nhân vật còn lại.

Hồ sơ chi tiết: graphics/models/bum07/PRODUCTION-BRIEF.md. Nguồn đã push: d7dd7e4 (asset + Blender source), 52dcdb0 (A/B/C + adapter + tests). Main giữ c3567aff87ce54adfa251895cecc2247c4d4b705. Bản Showcase đang triển khai vẫn là version 2; chưa tuyên bố đã cập nhật C lên link đó.

## Kết quả xuất ảnh đã xác nhận

Workflow run 42977152181 kết thúc completed/success trên commit 55c028b7c8791108ed747253119884583306bc7a. Các bước export và upload artifact đều success.

Artifact: bum07-C-six-renders, ID 13835319174, 1,472,480 bytes, digest sha256:412abfcc6608021d816c1186811cb650a822ca8b5890d3f28045481fabf050c8. Lưu trên GitHub Actions 30 ngày (hết hạn 11/12/2026); đã tải bản ZIP qua connector để bàn giao.

Link tải đã xuất hiện trong log upload-artifact:
https://github.com/minhhuypdk/be-bum-penalty/actions/runs/42977152181/artifacts/13835319174

ZIP chứa sáu PNG approval-front/45/profile/back/face/kick, approval-render-manifest.json và index.html tổng hợp. CI xác nhận đủ góc, source/asset hashes giữ nguyên, ảnh Kick khác Idle, không page errors và zero Supabase requests. Chất lượng mỹ thuật vẫn chưa đạt/nghiệm thu, không dùng success CI làm điểm 9/10.

Showcase live vẫn version 2 A/B Snow. Không triển khai C/gallery lên Site trong lúc môi trường Codex unavailable. Không đưa link live cũ làm bằng chứng đã xuất bản C.

## Tiếp tục khi môi trường có lại

Giữ nguyên checkout/worktree và các PNG/manifest/gallery cục bộ chưa commit. Không reset hard, clean hoặc tạo lại dự án. Nhánh remote đã tiến từ 52dcdb0 qua các commit CI/docs trong lúc executor offline: cần bảo toàn thay đổi local/untracked trước fetch/pull và giải quyết khác biệt test script, không ghi đè nguồn.

Khôi phục môi trường hiện có, nhận artifact ZIP, giữ ảnh mốc; kiểm tra lại mock regression tới exit status cuối và chuẩn bị đúng allowlist/gallery. Khi triển khai Site, đọc lại audience hiện hành, giữ project ID và version 2 để rollback; không merge PR #2, không sửa main/game GitHub Pages hoặc Supabase. Chưa có FPS iPhone thật hoặc clip Jump.
