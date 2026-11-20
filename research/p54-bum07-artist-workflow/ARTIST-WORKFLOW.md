# P5.4 — Artist workflow đề xuất, chưa triển khai

## Vai trò và điều kiện bắt đầu

Chủ dự án chọn **A/R hoặc B/base ngoài** trước. Mọi bước bên dưới cần được cho phép riêng khi tới giai đoạn đó; chấp nhận báo cáo P5.4 không tự cho phép sculpt/rig/GLB/integration. Không có artist được thuê trong phiên này.

Người thao tác Blender (chủ dự án hoặc artist được duyệt sau) quyết định và sculpt form, chỉnh loops/UV và tạo biểu cảm. Codex hỗ trợ scene/reference/camera, provenance, audit, đo kết quả, render lặp và đóng gói; không giả nhận thao tác thủ công hoặc bảo đảm đạt9/10. Không viết tiếp generator khuôn mặt bằng Python. Nếu thiếu người sculpt, dừng ở kế hoạch thay vì chạy lại cách procedural.

Nguồn mỹ thuật duy nhất là B — Gió Sân Cỏ trong P5.1/P5.2R. [Hướng dẫn P5.2R](../p52r-bum07-design-lock/MODEL-CONSTRUCTION-GUIDE.md), [design-spec](../p52r-bum07-design-lock/specification/design-spec.json), [proportions](../p52r-bum07-design-lock/specification/proportions.csv), [palette](../p52r-bum07-design-lock/specification/palette.csv) giữ nguyên; đây là mốc thiết kế, không phải mọi số đã đo từ mesh.

- H = đỉnh sọ–cằm neutral, không tóc; mục tiêu sọ–đất5H, tóc tối đa5.2H theo hồ sơ cũ. Không đổi mốc để hợp một donor.
- +Z lên, −Y hướng mặt, +X trái giải phẫu. Ngôi trái nhân vật = bên phải ảnh front, bên trái ảnh back. Mái quét thấp sang phải nhân vật; 5–7 cụm lớn là ý đồ phân khối, không số object/polygon bắt buộc.
- Oval mềm trẻ em, mắt hạnh nhân nâu, má/mũi/môi bo vừa; không hàm góc trưởng thành, đầu sơ sinh hoặc mắt anime tròn khổng lồ.
- Vàng `#F6C744`, navy `#182B45`, tóc `#241D1A`, da `#D9A078`; giữ bảng màu đầy đủ trong palette cũ. Không lấy sample vùng highlight AI thay màu vật liệu.

## G0 — Chọn hướng và provenance

Sau khi chủ dự án chọn, tạo working copy/branch mới từ checkpoint đã duyệt, donor gốc immutable + SHA + URL/license. Nếu A: R làm file làm việc, B1 chỉ tham chiếu lỗi/orbital; không ghép mặt B1 lên R rồi gọi nâng cấp. Nếu B: chọn chính xác Head Generic hoặc donor khác đã được duyệt, không nhập cả bundle/rig một cách mù quáng.

Kiểm nguồn/notice của mesh/material/texture/code tách riêng; giữ text Rain notice trong chứng cứ, chỉ dùng grant của đúng asset. Disable autoexec khi audit; không chạy rig script lạ để “fix” file. Nếu chọn Spring, dùng phiên bản Blender/BlenRig đúng để kiểm, sau đó mới lập cách chuyển export rig. Không tự cài subscription hoặc mua Source.

**Đầu ra:** manifest nguồn, scene thướcH, reference ảnh B, camera thật và kế hoạch thay đổi. **Dừng** nếu binary khác hash, thiếu quyền phân phối hoặc khác asset đã duyệt.

## G1 — Nghiệm thu silhouette

Làm khối lớn bằng thao tác Grab/Clay/Scrape thủ công trên working copy; không sculpt pores hoặc vật liệu đẹp trước. Từ R: giảm phụ thuộc vào khối cũ, xử lý oval/profile/cằm trước. Từ Head Generic: tạo nét trẻ em mới theo B; không chọn preset anime hay scale người trưởng thành làm BUM.

Render clay/roughness đơn giản bằng ORTHO0/45/90/180, target/scale/đèn cố định, ảnh1200×1600 hoặc lớn hơn; thêm góc cao/thấp để tìm lỗi. Giữ một model cho mọi góc, có thước1H/đường trán–cằm. Dùng R toàn thân làm đối chứng5H; không tuyên bố bust đã đo toàn thân mới.

**PASS đề xuất:** oval/trán–má–hàm đọc đúng nét trẻ, profile cằm không thành mấu, tai/mũi có chiều sâu hợp lý; không trưởng thành hơn B. Chủ dự án duyệt ảnh riêng. **FAIL:** chỉ đẹp front, profile méo hoặc dùng phối cảnh/che mesh để tránh lỗi. Chưa G2 nếu chưa duyệt G1.

## G2 — Nghiệm thu khuôn mặt

Sculpt thủ công hốc mắt, khóe và bờ mí trên/dưới liên tục; globe làm thước tiếp xúc, không phóng iris để tạo cảm xúc. Dùng các mốc mắt/môi P5.2R làm điểm xuất phát, vẫn cần phán đoán mỹ thuật. Tạo nose tip/alar, má, philtrum, môi có volume và khóe cắm tự nhiên vào má. Giữ chuyển khối khi tắt SSS, không dùng specular/catchlight lớn che thiếu form.

Render cận mặt neutral0/45/90, clay và vật liệu cơ bản, cùng setup G1. Overlay các đường landmark như guide, không ép khớp từng pixel ảnh AI. Nếu phải thay số đo thiết kế, ghi lý do/delta và xin chủ dự án duyệt; không sửa hồ sơ cũ.

**PASS đề xuất:** mắt hạnh nhân có thần thái, không lồi/quá nhiều sclera ở45/90; môi/mũi/má tự nhiên, giữ nhận diện B ở mọi góc. Không gọi manifold/UV/export thành công là PASS mỹ thuật. Chờ duyệt khuôn mặt trước G3.

## G3 — Nghiệm thu tóc

Dựng và sculpt bằng tay các khối từ part trái, đỉnh, mái chính/phụ, thái dương và gáy theo B. Chân tóc có hướng mọc; taper mềm và khoảng âm vừa phải; không cap tròn đều hoặc dải/rãnh song song. Có thể dùng curve hướng dẫn thao tác nhưng phải đánh giá mesh/volume thật; không giữ topology donor để bảo toàn rãnh xấu.

Render0/45/90/180 và góc cao/back kiểm part/hairline/gáy, cả clay lẫn vật liệu nâu chuẩn. **PASS:** mái thấp, part đúng trái giải phẫu, silhouette/chiều sâu mềm và ổn định, gáy trên cổ áo; không như mũ/ống nhựa. **FAIL:** chỉ thêm subdivision/normal map hoặc ánh sáng đẹp. Chờ duyệt tóc trước bước topology/biểu cảm.

### Sau G2/G3 đã duyệt — chuẩn bị topology biểu cảm

Tạo low cage/retopo có loops quanh mắt/miệng, luồng má–khóe; poles tránh vùng gập, mouth interior/teeth tách vai trò; giữ sculpt high riêng. Base có quad chỉ là khởi đầu, không chứng minh deform. Với Head Generic, giữ loops tốt nếu còn phù hợp; không cố bảo toàn khi sculpt đổi form lớn. Voxel/remesh chỉ trong bản sao và phải kiểm mất mí/môi; không decimate để giả retopo.

UV/bake kiểm distortion/seams, chuyển UDIM nếu có thành texture layout game phù hợp. Tạo một cung răng trên8 răng theo sơ đồ P5.2R, không khe giữa chủ ý; không biến răng AI thành hàng trắng phẳng. Chưa full-body rig.

## G4 — Nghiệm thu biểu cảm

Một model/một facial setup; chọn blendshapes hoặc facial bones + corrective có lý do. Tạo8 trạng thái Neutral, Happy, Big Smile, Blink100%, Focused, Surprised, Disappointed, Celebration. Cùng0/45 cho từng trạng thái; Focused tự tin, không giận; Celebration mắt vẫn có hồn. Upper teeth giữ một cung; môi/má/jaw giữ volume, đầu không đổi người.

- Blink0/25/50/75/100% ở0/45, thêm90 nếu có nghi ngờ. Kiểm contact/va chạm và ảnh vùng mí ở độ phân giải/DPR đã khai báo. Blink100% còn thấy iris/sclera bất thường: **FAIL**, không dùng hide/globe shrink/mesh phủ. Không kế thừa PASS Blink từ P3/P4/R.
- Smile0/50/100%: khóe nâng cùng má, môi có volume, răng không đổi số/cung và không xuyên; không nụ cười đường phẳng. Kiểm kết hợp Smile+Blink để phát hiện corrective thiếu.
- Lưu ảnh, shape-key/bone values, intersection report, native editable. Rig Blender chỉ là kiểm tra native; chưa gọi GLB đã đạt.

**Dừng để chủ dự án duyệt biểu cảm riêng**; kỹ thuật không thay thẩm mỹ. Nếu phải sửa silhouette/face/hair đáng kể, quay lại xin duyệt đúng checkpoint bị ảnh hưởng, không âm thầm thay.

## G5 — Nghiệm thu toàn thân

Chỉ sau khi phần đầu/tóc/biểu cảm được duyệt, làm body/neck/shoulders/5 ngón/legs/boots/kit trên working copy. Đo skull-to-floor5H, mốc vai/hông/gối theo P5.2R; hair-height báo riêng. Dung sai kiểm thử đề xuất5H±0.05H, cần chủ dự án duyệt như ngưỡng QA, **không thay thiết kế cũ**. Không dùng scaling riêng camera hoặc bóng đổ che bàn chân.

Áo vàng07 rõ trên bề mặt, cổ V navy phía trước/bo sau, raglan piping/nếp vải hợp lực, navy shorts, tất sáng/giày bóng đá. Sau lưng không sponsor; tên/số theo hồ sơ khóa. Render fullbody0/45/90/180, A-pose và face crop giữ nhận diện. **PASS:** nét trẻ, đầu–cổ–vai hài hòa và một nhân vật ở mọi góc, chất liệu đẹp không plastic; năm ngón và giày đọc được. Xin duyệt toàn thân trước hoàn thiện rig/budget.

## G6 — Cổng kỹ thuật tương lai, không nằm trong P5.4 đã thực hiện

Sau các duyệt mỹ thuật và cho phép kỹ thuật riêng: body rig, weights/correctives, test joint extremes; xuất GLB thử nghiệm so native, rồi mới cân nhắc game. Không xóa joints/cắt influences để vượt kiểm tra mà không chứng minh biến dạng tương đương.

Targets lập kế hoạch, **chưa đo/không là cam kết iPhone**:

| Hạng mục | Đề xuất và điều kiện |
|---|---|
| LOD | Bắt đầu LOD0≈50–80ktri/nhân vật, LOD1≈25–40k, LOD2≈10–18k. Chỉ giảm sau so ảnh/khoảng cách; giữ silhouette/mí/tóc, không ưu tiên con số hơn chất lượng |
| Draw calls | Hướng tới6–10 material primitives/nhân vật, atlas hợp lý. Đo `renderer.info.render.calls` cả frame/shadow passes; không lấy số slot Blender làm draw calls |
| Texture | Đầu/body2K khi cần, bake PBR/normal/ORM; KTX2/Basis kiểm trên Safari với extension/fallback thật. RGBA8 2K+mips≈21.3MiB/map chưa nén GPU; dung lượng GLB không là VRAM |
| GLB | Mục tiêu khởi điểm8–15MB/nhân vật, báo bytes thực và peak decode; geometry/texture compression chỉ giữ khi so ảnh/deformation không giảm chất lượng |
| Skin | Khởi điểm4 influence nếu phép so skin chứng minh đủ; báo weighted joints/nondeform joints trước/sau. Không đặt số bones thấp để tự pass |
| WebKit/Chromium | Cùng asset/góc/DPR, kiểm iris/Blink/Smile/UV/skin sau xuất thực tế. Desktop WebKit không thay Safari iPhone |
| Thiết bị thật | iPhone tối thiểu do chủ dự án xác định sau; ghi model/iOS/Safari/DPR/độ phân giải/chất lượng/thermal. Test5phút với2 nhân vật và sân thật; mục tiêu≥30FPS ổn định, báo median/p95 frame time/load/memory thay vì suy từ CPU render |

Nếu chưa có thiết bị, đánh dấu NOT_TESTED, không tự PASS iPhone. Không giảm nét mặt chỉ để đạt FPS; tìm bottleneck shader/material/shadow/texture trước. Bản GLB thử nghiệm cũng chỉ tích hợp game sau quyết định riêng, không tự merge PR #2 hoặc sửa Pages/Supabase.
