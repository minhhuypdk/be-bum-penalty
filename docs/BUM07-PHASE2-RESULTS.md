# BUM 07 Phase 2 — kết quả bàn giao đã xác nhận

Art gate: CHƯA NGHIỆM THU, chưa xác nhận 9/10. Computational mesh-edit/blockout, không phải sculpt thủ công chuyên nghiệp. Chỉ mặt/tóc; chưa chuyển body hoặc animation.

## Artefact có thật

Run 42983794384 completed/success trên commit 6006c45ba6ac16aa872fb60038d9943388d6657f.
https://github.com/minhhuypdk/be-bum-penalty/actions/runs/42983794384

Artifact bum07-P2-face-hair-artist-review, ID 13838836950:
https://github.com/minhhuypdk/be-bum-penalty/actions/runs/42983794384/artifacts/13838836950

23,257,790 bytes; digest sha256:97f1d6f1f14fa64e269819b8d8592a2e467d056a757e260513899486202e12fa.
Đã tải bản ZIP qua connector. GitHub giữ 30 ngày, hết hạn 11/12/2026; nên lưu bản bàn giao riêng.

ZIP gồm index.html bốn cặp C/P2 front/45/profile/close, PNG/morph study và comparison.json; thư mục artist có workbench Blender editable, hai GLB, manifest, audit, source-audit.json và GUIDE.md. C bên trái/P2 bên phải dùng cùng studio/camera 35° và neutral tĩnh; ảnh là canvas render thật, không phải concept AI.

## Kết quả đọc lại và render

Job source audit mở C và workbench độc lập bằng Blender 4.3.2, PASS:
- 44 mesh ngoài phạm vi giữ geometry/UV/material/skin weights.
- Bones/actions và C-head-reference không đổi.
- Có head geometry edit thật, body khóa chọn, 10 hair guide, 6 reference PNG packed.
- Khối tóc sculpt không có open boundary.

Browser PASS bốn cặp render, morph studies tĩnh, source/asset hashes giữ nguyên và zero Supabase requests. Đây là kiểm chứng dữ liệu/renderer, không phải điểm mỹ thuật hoặc FPS iPhone. Chưa có đo trên thiết bị thật.

## Phần artist cần hoàn thiện

Anatomy/chuyển tiếp mí/hốc mắt/môi, weld/retopo seams; cân biểu cảm và loại xuyên globe khi blink; sculpt silhouette/roots/layer tóc, retopo/bake mặt/tóc. Không gọi hair blockout hoặc script là tóc/mặt điện ảnh hoàn chỉnh. Xem docs/BUM07-PHASE2-ARTIST.md và artist/GUIDE.md trong ZIP.

## Bảo toàn dự án

Commit Phase 2 chỉ thêm generator/test/guide/workflow. Không thay mã Showcase A/B/C dùng chung hoặc file A/B/C; không deploy và không merge PR #2. Main vẫn c3567aff87ce54adfa251895cecc2247c4d4b705; game GitHub Pages và Supabase không đổi. Showcase live vẫn version 2 A/B Snow, không gán link đó cho P2.

Môi trường Codex lại unavailable trước khi push các file local; gói trên được dựng lại độc lập bằng GitHub Actions từ nguồn C đã lưu. Khi môi trường trở lại, bảo toàn worktree, ảnh và các thử nghiệm chưa commit trước fetch/pull; không reset hard/clean hoặc tạo lại dự án. Các thay đổi cục bộ và phiên bản CI có thể khác nhau, cần đối chiếu hash, không ghi đè bản artist.

Dừng ở mặt/tóc và chờ nghiệm thu hình ảnh trước khi phát triển body/animation.
