# BUM 07 — Hồ sơ sản xuất dành cho artist Blender v1.0

**P2 CHƯA NGHIỆM THU. Không tạo P3/P4 bằng chỉnh mesh tự động. Hồ sơ này không phải mô hình mới hoặc xác nhận đạt 9/10.**

## Bàn giao và nguồn chuẩn

Dùng nguyên byte `bum07-facehair-workbench.blend` từ artifact P2 run **42983794384**, artifact **13838836950**, source commit **6006c45**. SHA-256 workbench: `30338d105c61eb206b688d31d74f9a7ccd947607f7ad67a5aff89833a8cb2f4c`.

Trong repository, bản gốc nằm tại BASELINE-P2/artist/bum07-facehair-workbench.blend. Trong ZIP, bản này được sao chép sang SOURCE/bum07-facehair-workbench.blend.

Gói hồ sơ phải có file này thật trong `SOURCE/`, không chỉ đường dẫn hoặc hướng dẫn tạo lại. Mở bằng Blender **4.3.2 trở lên**, không cần bật Auto Run Python. Nguồn đã được mở đọc kiểm tra; đóng gói không Save/Remesh/đổi geometry, không chạy generator. Các GLB và render P2 cũ chỉ là reference, không phải sản phẩm được duyệt.

- `design-spec.json`: nguồn duy nhất của tỷ lệ/landmark đề xuất.
- `production-brief.html` và PDF: tài liệu đọc/print, gồm sơ đồ tỷ lệ 2D, ảnh lỗi, quy trình và checklist.
- `issue-backlog.csv`: lỗi có mức ưu tiên, người thực hiện, đầu ra và điều kiện đóng lỗi.
- `acceptance-checklist.csv`: từng cổng nghiệm thu, mặc định OPEN, không tự gán PASS mỹ thuật.
- `SCOPE-AND-RESPONSIBILITY.md`: phân công Codex/artist/chủ dự án và giới hạn phạm vi.
- `REFERENCES/`: ảnh C/P2 và metadata gốc, không retouch.
- `MANIFEST.json` và `VALIDATION.json`: hash file, nguồn, kiểm tra gói; PASS ở đây chỉ là tài liệu/file hợp lệ.

## Hướng thiết kế thống nhất — ĐỀ XUẤT, chưa được duyệt

Chỉ BUM tiền đạo số 07: trẻ em tự tin, dễ thương, tự nhiên. Giữ mắt nâu, tóc nâu đậm ấm, áo vàng 07 và quần navy; không thay nhận diện bằng cách đổi tông da, giới tính, tuổi, logo hoặc tạo một nhân vật khác. Thân/trang phục/rig toàn thân và ba nhân vật còn lại khóa phạm vi.

Dùng **H = chiều cao sọ từ cằm tới đỉnh sọ, không gồm tóc/tai**. Gốc ở giữa đáy cằm; +X là trái nhân vật/phải người xem ở chính diện, cao độ theo +Z Blender. Phía trước là -Y Blender. Không đưa tỷ lệ toàn thân mới vào giai đoạn này.

Một bảng mục tiêu được thống nhất trong JSON: rộng đầu 0,92H, sâu sọ 0,80H; tâm mắt ở cao độ 0,56H, khe mắt 0,23×0,13H, khoảng khóe trong 0,15H; iris 0,105H, pupil 0,045H. Mũi nhỏ, đầu mũi ở 0,43H, bề ngang cánh 0,115H và projection tối đa 0,055H. Đường môi ở 0,285H, rộng neutral 0,25H. Tóc thêm tối đa 0,08H ở đỉnh, mái thấp nhất 0,76H; ngôi trái nhân vật, quét sang phải nhân vật.

Đây là **một đề xuất nhất quán** để artist không tự suy diễn nhiều tỷ lệ mâu thuẫn; chưa có phê duyệt thiết kế từ chủ dự án. Artist đo bằng orthographic technical view. Số đo đúng không đồng nghĩa đẹp: clay front/45/profile phải được chủ dự án duyệt trước khi retopo và PBR chi tiết. Nếu cần đổi tỷ lệ, ghi mục thay đổi và xin duyệt bằng ảnh; không âm thầm áp dụng bộ số khác. Không dùng JSON để auto-deform hoặc sinh biến thể mesh.

## Các lỗi chặn sản xuất

**P0 — phải xử lý trước retopo cuối/PBR:** form mắt nổi và mí như patch; tóc vỏ/plank/giao cắt; mũi–miệng–má thiếu chuyển tiếp/cá tính trẻ em. Không sửa bằng ánh sáng hoặc vật liệu che seams. P2 vẫn có thể gần một vài tỷ lệ đề xuất mà chưa đạt form.

**P1 — trước facial rig/GLB nghiệm thu:** retopo loop mí/môi, normals và seams; cleanup brow/lip/cheek; facial shapes không xuyên globe và không phá neutral; bố trí chân tóc/khối phụ rõ ở góc nghiêng.

**P2 — sau khi clay/form duyệt:** UV/PBR, hair bake và LOD có bảo vệ silhouette/morphs; kiểm tra Safari iPhone thật. Không dùng low texture memory hoặc Linux software FPS làm bằng chứng chất lượng hay độ mượt.

Lỗi áo bị kéo gãy trong ảnh Kick được ghi nhận nhưng **ngoài phạm vi hiện tại**. Không sửa áo, thân, chân, animation hoặc ba nhân vật khác trong gói này.

## Dùng workbench hiện có

Lưu một bản làm việc artist riêng, không ghi đè file SOURCE nguyên byte. Không chạy `build-bum07.py` hoặc `prepare-bum07-facehair.py` để sinh bản mới.

- `00_C_LOCKED_FACE_REFERENCE`: mặt/tóc C ẩn, khóa chọn; không sửa.
- `01_P2_FACE_HAIR_EDIT`: head, eyes/lids/brow/lips và hair blockout để artist xử lý.
- `02_P2_HAIR_RAW_GUIDES`: 10 guide P2 ẩn. Đây là guide nghiên cứu, không bắt buộc giữ số lượng hoặc shape trong final; bố cục master đề xuất 3 khối chính + 5 khối phụ.
- `03_C_BODY_OUTFIT_LOCKED`: 44 mesh ngoài phạm vi, giữ khóa.
- Sáu `C_REFERENCE_approval-*.png` đã packed; mở trong Image Editor.
- `ART_Front/ART_45/ART_Profile` là camera thao tác artist, **không phải camera nghiệm thu matched-render**; không lấy khác biệt lens làm cải thiện.

## Sculpt và retopology — artist thực hiện

1. Dựng clay form đầu/mặt/tóc theo master. Xem front/45/profile đồng thời, giữ nhận diện BUM. Dùng volume và plane mềm cho trẻ em; không lấy mặt trưởng thành rồi thu nhỏ.
2. Head có shape keys: duplicate thành bản high-poly riêng. Chỉ remove keys/remesh/Dyntopo trên bản sao; không phá vertex order bản keyed hoặc C-reference. Không remesh toàn nhân vật.
3. Sửa socket/globe trước: globe nằm sâu, corneal apex không vượt orbital rim plane quá 0,025H theo đề xuất; mí ôm globe, có góc mắt và thickness, không phải hai mảng dán lên mặt. Đo projection trong profile, kiểm tra cả mở/nhắm mắt.
4. Sculpt mũi nhỏ, bridge–tip–alar/philtrum hòa vào má; môi có cupid/vermillion vừa phải, khóe thật, không vệt đen. Neutral thư thái; smile ảnh hưởng má/khóe chứ không chỉ kéo môi.
5. Tóc: thiết kế root/flow từ ngôi trái nhân vật sang phải, 3 mảng lớn + 5 phụ, độ sâu/taper thật. Loại giao cắt, dải nổi không bám scalp và hard shell silhouette. Sculpt bằng khối có chủ đích, không thêm ống hoặc chỉ tăng subdivision. Retopo/bake sau khi duyệt khối.
6. Retopo thủ công: quad flow quanh mắt/môi; loop phù hợp blink/smile; đủ mật độ tại khóe/mí và transition vào cheek. Bridge/weld annulus–face đúng topology, sửa normals. Không đặt Merge by Distance lớn làm sụp mí. Không có loose vertex/degenerate face/ngược normal hoặc z-fighting nhìn thấy.
7. Tách high/low. UV không bleed ở mí/môi; chuyển vertex color/texture có kiểm tra. Không thay geometry/UV/material/weights ngoài mặt/tóc. Sửa tóc/đầu không được kéo cổ/vai/thân theo.

## Facial rig — phạm vi khuôn mặt, không làm sports animation

P2 `FH_Blink/FH_Smile` là nghiên cứu chưa duyệt. Artist xây neutral Basis đúng trước; các shape không được che lỗi base mesh. Đề xuất production targets: `eyeBlink_L/R`, `smile_L/R`, `browUp_L/R`, `browDown_L/R`, `jawOpen` nếu được duyệt trong phạm vi facial rig. Có thể dùng bones/shape keys kết hợp, nhưng runtime GLB phải tái hiện được; không phụ thuộc một driver Blender không được bake/export.

Giữ nguyên tên/rest matrix của các body bones hiện có, kể cả Head/Neck, weights ngoài mặt và bốn action C. Nếu thêm facial bones, chỉ thêm nhánh `FACE_*` dưới Head, ghi whitelist; không dùng audit equality toàn armature cũ để phủ nhận mọi facial bone mới, nhưng toàn bộ bones cũ phải giữ nguyên. Không thêm/chỉnh timeline Run/Kick/Celebrate.

Kiểm tra tĩnh neutral, soft smile, focus và blink ở 0/50/100%; mắt không xuyên mí, mí không collapse; môi/khóe/má phối hợp, hai bên độc lập và phối hợp ổn. Nếu cần jawOpen, kiểm tra lips/teeth/tongue theo phạm vi đã duyệt, không mở rộng thành lipsync/animation mới.

Giao `facial-target-map.json` ghi tên target/bone/range và neutral. Adapter hiện tại chỉ có study aliases FH_Blink/FH_Smile; Codex phải tích hợp mapping sau khi có asset phù hợp, **không khẳng định tên mới tự chạy trong viewer hiện có**.

## Vật liệu và GLB

Sau clay/form duyệt: albedo đúng sRGB; normal/roughness/AO ở non-color; kiểm tra tangent/MikkTSpace và UV seams. Da/tóc có roughness tự nhiên, không vẽ highlight để che form. Màu mắt/tóc/da giữ nhận diện. Không tự đổi exposure/LUT hoặc HDRI trong ảnh so sánh. Ưu tiên khối tóc opaque phù hợp phong cách; hair cards/alpha cần đề xuất riêng và đo overdraw, không mặc nhiên thêm để gọi là chuyên nghiệp.

Giữ `.blend` editable với high/low, UV, textures packed, facial rig/targets và mapping. Xuất **GLB 2.0 nhúng texture**, +Y Up như glTF chuẩn; tên version artist riêng, không overwrite A/B/C/P2. Chỉ chọn các mesh/skin cần xuất; loại reference/camera/light/helper khỏi runtime; không tự apply Armature làm mất skin hoặc apply topology modifier sau shape keys rồi mất morphs. Bake/convert constraints cần thiết sang dữ liệu mà glTF hỗ trợ; kiểm tra lại GLB trong viewer độc lập.

Kiểm tra animation export: chỉ giữ nguyên các action C đã có nếu cần đối chiếu, không bake thêm camera/reference hoặc sinh clip mới. Không đính kèm script auto-run. Draco/Meshopt/KTX2 chưa mặc nhiên có decoder ở viewer; bản giao đầu cần tương thích không nén này, tối ưu sau bằng Codex và kiểm tra thật.

LOD mặt/tóc chỉ làm sau duyệt silhouette: bảo vệ mí/môi, roots và vertex/morph mapping. Budget phải ghi riêng cho phần mới và carrier C; không decimate toàn đầu vô điều kiện hoặc hạ chất lượng chỉ để tăng FPS. Chưa chốt budget cứng hay FPS iPhone trước asset được duyệt và có đo thiết bị.

## Nghiệm thu bằng ảnh

Bắt buộc bốn cặp **P2 gốc / bản artist**: chính diện 0°, 45°, nghiêng 90°, cận mặt. Dùng cùng GLB review studio, camera vertical FOV 35°, viewport 1500×1100 DPR1, framing/angle/target từ `REFERENCES/comparison.json` (canvas thực khác viewport do sidebar). Close dùng cùng mức zoom của reference. Không rescale ảnh độc lập, thay pose, lens, light, grading, denoise hoặc retouch để che lỗi.

Xuất PNG lossless theo kích thước canvas trong metadata, giữ neutral/Idle time 0; ảnh face và hair phải nằm trong khung. Thêm clay orthographic technical sheet để đo tỷ lệ, **không thay bốn matched renders bằng orthographic rồi so với ảnh perspective**. Nếu dựng camera Blender, chuyển trục Three(x,y,z) sang Blender(x,-z,y), khớp target/FOV/aspect; camera ART_* 55mm trong file không tự bằng 35° protocol. Cách đáng tin hơn: Codex tải GLB artist vào cùng test viewer và xuất lại bốn góc.

Nộp thêm ảnh soft smile/focus/blink tĩnh để kiểm facial rig, cùng lighting. Ghi commit/file SHA, source `.blend`, GLB, textures/mapping, render settings và ảnh trước/sau. Không dùng ảnh concept AI làm bằng chứng mesh.

**PASS kỹ thuật không phải PASS mỹ thuật.** Artist tự kiểm checklist, Codex kiểm dữ liệu/export/render, chủ dự án duyệt trẻ em/dễ thương/nhận diện/form/biểu cảm. Không tự chấm 9/10. Chỉ khi chủ dự án duyệt bằng ảnh mới mở body/animation hoặc ba nhân vật còn lại.

## Mở hồ sơ và tái tạo gói bàn giao

- `BUM07-ARTIST-PRODUCTION-v1.pdf`: hồ sơ đọc trực tiếp, gồm sơ đồ đề xuất và ảnh C/P2 gốc.
- `BASELINE-P2/artist/bum07-facehair-workbench.blend`: file Blender thật, giữ nguyên byte; không phải model mới.
- Workflow `BUM07 artist production dossier` tạo ZIP gồm PDF, nguồn Blender, sơ đồ SVG, ảnh reference, CSV và manifest SHA-256. Workflow này không gọi Blender hoặc script tạo mesh, không triển khai game.
- Quy trình P2 cũ chỉ còn chạy thủ công để lưu khả năng tái lập lịch sử; không tự chạy khi push. Không chạy lại để tạo phiên bản mỹ thuật mới trong phạm vi hồ sơ này.

Chạy `prepare` bằng `scripts/package-bum07-artist-dossier.py`, xuất PDF bằng `scripts/render-bum07-artist-dossier.cjs`, rồi chạy `finalize` để kiểm tra và đóng ZIP. Đường dẫn nguồn là `docs/artist-production/BUM07/BASELINE-P2`; đường dẫn output phải ở ngoài thư mục nguồn. Cần Python 3, Node, Playwright và Chromium. Tham khảo workflow để có lệnh đầy đủ.
