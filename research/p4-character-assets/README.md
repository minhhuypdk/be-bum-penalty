# P4 — Character Asset Replacement Research · BUM07

**Chỉ khảo sát, chưa chọn/đổi asset game và chưa tạo BUM từ asset.** Chủ dự án đã nghiệm thu riêng Blink100% P3.1R, không nghiệm thu mỹ thuật tổng thể. C/P2/P3.1/P3.1R giữ nguyên. Baseline `7ef3218`; nhánh riêng `research/p4-character-assets`; PR#2 không sửa/merge.

[Đọc PDF hồ sơ](ASSET-CANDIDATES-P4.pdf) · [Gallery HTML trong ZIP](index.html)

## Đề xuất trước khi làm thử

Ưu tiên chủ dự án xem **Scott nguyên bản** trước: là cậu bé phù hợp hướng BUM hơn Snow trưởng thành, có file nguồn miễn phí và giấy phép tác giả rõ. Tuy nhiên rig chưa game-ready, khuôn mặt/tóc vẫn lộ faceting và chưa đạt9/10. **Storm** đáng cân nhắc về cấu trúc facial cao cấp nhưng có rào cản tải trả phí/phiên bản; **Spring** là tham khảo tạo hình trẻ em, cần redesign có chủ đích để thành BUM. **Quaternius Teen** hợp ngân sách kỹ thuật hơn nhưng preview quá trưởng thành/góc cạnh, không khuyến nghị làm chất lượng cuối.

| Ứng viên / nguồn gốc | Quyền và chi phí | Rig, facial, GLB | Đánh giá BUM |
| --- | --- | --- | --- |
| [Boy (Scott) — Mish7913](https://blenderartists.org/t/boy-scott-free-3d-character-mish7913/1510925) | Tác giả dẫn trực tiếp [CC BY4.0](https://creativecommons.org/licenses/by/4.0/) và `.blend` miễn phí. Cho game/chỉnh sửa/phân phối, phải ghi công và nêu thay đổi. | Đã kiểm file:370bones/557constraints/440drivers;0facial blendshape. Probe GLB23.701tris,8primitives,3.447.428bytes,370joints. | Ưu tiên xem ảnh; chưa đồng ý chọn. Child-boy thật, không thu nhỏ người lớn. Cần bake/simplify rig và kiểm lại Blink/Smile. |
| [Spring v1 — Blender Studio](https://studio.blender.org/characters/spring/v1/) | Trang chính thức ghiCC-BY/Free; registry nhà phát hành ánh xạCC-BY→BY4.0. Ghi công Foundation, link license/source, nêu sửa đổi. Chưa có binary để soát notices. | Publisher:Blender2.8–3.6+BlenRig. Polycount/morph/GLB chưa đo; cần bake controls và kiểm hair representation. | Nhân vật trẻ em nhưng nguyên mẫu là bé gái. Chuyển thành BUM cần thiết kế mặt/tóc/trang phục, không chỉ thay màu. |
| [Storm v1 — Blender Studio](https://studio.blender.org/characters/storm/v1/) | CC-BY theo trang chính thức và registryBY4.0. Trang tải hiện yêu cầuStudio subscription; chưa mua/tải, chưa chốt phí. | Publisher:Blender>=5.0; CloudRig body, facial hybrid shape keys/ribbon/lattice. Local4.3.2 không phải bản hỗ trợ; chưa audit file/GLB. | Hướng cậu bé có facial đáng nghiên cứu; hợp hơn dùng Snow nguyên mẫu. Bị chặn bởi access, version và chuyển đổi rig, chưa chấm chất lượng. |
| [Universal Base Characters — Quaternius, Teen](https://quaternius.com/packs/universalbasecharacters.html) | [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/); game/chỉnh/phân phối được, credit không bắt buộc. Standard miễn phí; Source`.blend` niêm yết$19.99 lúc kiểm. | Publisher:humanoid retargetable; trung bình13ktris, glTF/FBX. Chưa kiểm selected model/morphs. Standard vẫn edit được sauimport; không đồng nhất với native Source. | Không khuyến nghị cho tạo hình cuối vì preview trưởng thành/góc cạnh. Không thu nhỏ/recolor các body trưởng thành thành BUM. |

`candidates.json` tách số đo thực, tuyên bố publisher và trường chưa biết. **CC-BY của Studio được đối chiếu registry chính thức**, không suy ra từ chữ Free; kiểm notices/file cụ thể vẫn là gate trước tích hợp. Không sử dụng mô hình nguồn gốc/quyền mơ hồ.

## Ảnh xem trước

- Scott: [ảnh tác giả](previews/scott-preview.png); [5 góc GLB nguyên bản và P3.1R](comparison/). Đây là **Scott mặc đồ gốc**, không phải BUM07 hoặc prototype đã duyệt.
- Spring: [ảnh rig chính thức](https://studio.blender.org/files/public/1b/1bffff08b464375d842e7da43b4f5293/1bffff08b464375d842e7da43b4f5293-thumbnail.jpg) · [trang nguồn](https://studio.blender.org/characters/spring/v1/). Chỉ dẫn link; môi trường bị403 khi tải ảnh/binary, không giả đã cache/render.
- Storm: [ảnh production chính thức](https://studio.blender.org/files/public/thumbnail/6d/aa/6daa38275a899b7d6c81a0a3bd8bf696-1_m.webp) · [trang rig](https://studio.blender.org/characters/storm/v1/). Link tham khảo, chưa có binary/ảnh local được kiểm.
- Quaternius: [preview publisher](previews/quaternius-preview.jpg) gồm cả adult/superhero/Teen, không phải hình BUM.

Nếu link Studio yêu cầu quyền truy cập hoặc không tải được, xem mục blockers trong báo cáo; không dùng ảnh/model mirror để vượt quyền. File preview Scott/Quaternius và ảnh GLB trong gói mở được độc lập, không phụ thuộc Studio.

## Tài liệu và bằng chứng

- [Báo cáo kỹ thuật](REPORT.md): topology/rig/facial/export/LOD/iPhone, phần đã đo và phần chưa biết.
- [Ma trận giấy phép](LICENSES.md), [credits ảnh/asset](THIRD-PARTY-CREDITS.md), `candidates.json`, `evidence/studio-license-mapping.json`.
- `audits/scott-audit.json`: đọc file gốc bằng Blender4.3.2, không auto-run, không Save.
- `audits/scott-export-probe.json`, `audits/scott-glb-audit.json`: GLB original static probe, nguồn giữ hash. Cảnh báo skin4influences được ghi rõ; chưa chứng nhận hoạt ảnh tương đương.
- `renders/original-asset-preview.json`: camera/target, source hashes, ảnh và draw calls thật, WebKit WPE/Linux, zero request Supabase.
- `VALIDATION.json`, `MANIFEST.json`: kiểm gói; PASS ở đây không phải owner chọn asset hoặc art9/10.

## Gate tiếp theo — chưa thực hiện

1. Chủ dự án chọn hướng ngoại hình từ dossier này; không lấy im lặng làm đồng ý.
2. Chỉ sau chọn: soát file/license notices đầy đủ, bake/simplify/export rig; kiểm Blink0/25/50/75/100 và Smile0/50/100. Nghiệm thu Blink của P3.1R **không tự chuyển** sang donor mới.
3. Khi có quyền và phương án đạt kỹ thuật mới tạo thử BUM áo vàng07/quần navy trên nhánh nghiên cứu, xuất ảnh matched studio để chủ dự án duyệt. Không đổi game công khai.
4. Chỉ đo Safari iPhone khi có máy thật; số desktop/GPU string/GLB nhẹ không thay thử thiết bị.

Không thuê artist, không mua asset/subscription, không đổi main/Pages/Supabase hoặc ba nhân vật khác. Không merge PR#2 và không thay bất kỳ model game nào.
