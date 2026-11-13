# P4 — khảo sát kỹ thuật và phương án thay asset

## Kết luận ở mốc khảo sát

Chưa có donor được chủ dự án chọn; chưa tạo BUM07 từ donor và chưa thay model game. **Scott nguyên bản** đáng xem đầu tiên vì trẻ em/nam và giấy phép tác giả rõ. **Storm** có hướng facial chuyên sâu nhưng access/Blender version chưa đáp ứng. **Spring** là tham khảo thiết kế trẻ em, không thể gọi thành BUM chỉ bằng đổi màu. **Quaternius Teen** có tính portable nhưng preview chưa phù hợp tuổi/phong cách; loại khỏi đề xuất mỹ thuật cuối ở mốc này.

P3.1R Blink100 đã được chủ dự án nghiệm thu riêng. Kết quả đó gắn với file P3.1R cũ, không phải bằng chứng donor mới cũng Blink đúng. Mỹ thuật cũ vẫn chưa được duyệt. Không tự chấm9/10 cho bất kỳ asset nào.

## 1. Scott — đã đọc binary và xuất probe nguyên mẫu

Nguồn phát hành [Mish7913](https://blenderartists.org/t/boy-scott-free-3d-character-mish7913/1510925), liên kết chính tác giả tới [file `.blend`](https://projects.blender.org/3DMish/M7s-Assets-Library/raw/branch/main/data/characters/scott-3d-model.blend) và BY4.0. File tải8.950.124bytes; headerBlender3.0. Đã mở đọc bằng local4.3.2 với auto-exec disabled, không Save và giữ nguyên SHA-256. Hash chi tiết trong audits.

### Quan sát ngoại hình

Preview tác giả và GLB nguyên mẫu thể hiện một cậu bé có đầu/mặt hoạt hình, tóc nâu dựng, hốc mắt/miệng gắn vào form đầu dễ đọc hơn các vành P3.1R. Tuy nhiên ảnh cận vẫn lộ faceting/shading, tóc còn chóp góc cạnh và outfit phiêu lưu/bandana chưa phải bóng đá. Đây là ứng viên thẩm mỹ để chủ dự án chọn, không phải kết quả điện ảnh đã đạt.

### Số đo thực

| Chỉ tiêu | Giá trị |
| --- | ---: |
| Mesh cơ sở có trong file | 10, gồm2 bone-shape helpers không mặt |
| Tam giác cơ sở / probe GLB | 23.701 |
| Primitive / material slots trong probe | 8 / 8 |
| Native armature bones / flags deform | 370 / 370 |
| Weighted bone names tìm thấy | 340 |
| Constraints / armature drivers | 557 / 440 |
| Facial blendshape | 0 |
| GLB joints / embedded images | 370 / 1 |
| GLB probe dung lượng | 3.447.428bytes |
| Native source action | `boy_lib_actions`, frames1–85; chưa phân loại thành sports clips |
| Probe clips | 0, **do lựa chọn tắt export animation**, không suy ra source không có action |

Mesh chính`Plane`:5660faces/5004quads; phần khác có cả quads/tris. Chưa chứng nhận loop topology, manifold toàn bộ hoặc deformation ở khớp/mặt. Có bone tênjaw/eyes/open-close/brow nhưng chưa thử độ kín Blink theo rig gốc. Không được coi0blendshape là không có facial rig; đó là rig dựa bone/driver cần khảo sát.

### Kết quả xuất và giới hạn

Đã sửa context Object/Edit Mode trong script khảo sát để exporter chạy; không sửa geometry/trang phục gốc. GLB import/render tĩnh thật trong WebKit WPE/Linux, buffer/texture nhúng, không request Supabase. Cảnh báo quan trọng: exporter dùng4skin influences cao nhất rồi normalize; source có nhiều ảnh hưởng hơn4. Vì vậy **static export PASS không phải animation equivalence PASS**. Cần kiểm/prune/rebind hoặc bake bone influence trước khi dùng runtime.

Cảnh báo vertex color không được dùng trong node tree nên không xuất, và optional Draco library không có; probe là uncompressed GLB, không phụ thuộc Draco. Materials/AutoSmooth node geometry không được chứng nhận pixel-match Blender. Không tự chạy Python nhúng; các driver/UI đặc thù chưa được chứng nhận portable.

### Ảnh so sánh thực

`renders/` và `comparison/` có chính diện,45°,90°,cận và toàn thân **Scott nguyên bản vs P3.1R**. Cùng studio, FOV35°, viewport1500×1100 DPR1, normalized height2.2, camera/target khóa bằng cùng công thức cho mỗi cặp. Giữ pose gốc của mỗi asset (Scott static/rest, P3.1R Idle), không giả hai rig cùng pose/action. Chỉ đổi variant và góc; không thay exposure/material để che lỗi. Cận là framing chặt, không dùng để suy ra tỷ lệ mặt đo orthographic.

Không có áo vàng07/navy mới, không đổi mặt donor và không gọi Scott là BUM. Ảnh xuất có credit donor; shader conversion/weight-truncation vẫn là giới hạn nghiên cứu. Số draw calls/triangles ở từng khung nằm trong`renders/original-asset-preview.json`; full-body Scott probe ghi11calls,25.239rendered triangles gồm studio; GLB bản thân chỉ8primitives/23.701tris. Không đồng nhất hai số.

## 2. Spring — chỉ đánh giá nguồn công bố

[Trang rig chính thức](https://studio.blender.org/characters/spring/v1/) xác nhận nhân vật trẻ em trong phim, gắnCC-BY/Free, hỗ trợBlender2.8–3.6 vớiBlenRig. Đã đối chiếu nhãnCC-BY với registryBY4.0 của publisher; chưa tải/mở binary nên chưa soát hết notices riêng.

Chất lượng film/face cần xem qua [preview rig chính thức](https://studio.blender.org/files/public/1b/1bffff08b464375d842e7da43b4f5293/1bffff08b464375d842e7da43b4f5293-thumbnail.jpg). Cô bé phù hợp hướng trẻ em hơn Snow trưởng thành, nhưng không đồng nghĩa phù hợp nhận diện BUM nam. Cần thiết kế lại hair/face/football garments có chủ đích, không thay màu hoặc thu nhỏ.

Topology, polycount, morph inventory, dạng hair và GLB chưa được đo. Nếu dùng legacy hair/constraints/driver cần bake/convert và kiểm deform; không giả glTF hỗ trợ BlenRig UI. Cần standalone Blender được rig hỗ trợ; local4.3.2 không được coi đã test tương thích. Không tự tải từ mirror.

## 3. Storm — ứng viên facial có rào cản

[Trang chính thức](https://studio.blender.org/characters/storm/v1/) và [bài phát hành](https://studio.blender.org/blog/storm-has-been-released/) công bố rig dùngCloudRig và kết hợp shape keys/ribbon/lattice cho mặt, yêu cầuBlender>=5.0. NhãnCC-BY ánh xạBY4.0 qua registry; quyền sử dụng asset khác chi phí truy cập file. Trang tải hiện yêu cầuStudio subscription, chưa mua/tải.

Có [preview production chính thức](https://studio.blender.org/files/public/thumbnail/6d/aa/6daa38275a899b7d6c81a0a3bd8bf696-1_m.webp) để xem thiết kế boy/youth. Cần chủ dự án duyệt độ tuổi/biểu cảm, không mặc định đạt9/10. Chưa biết triangle count, joints, texture và GLB bytes. Trang có attachment`gaming_animation_pack.blend`61.5MB/B5.3; **không dùng số đó làm dung lượng rig chính hoặc GLB**.

Chuyển facial sangglTF cần bake hình dạng/bones thay vì mang lattice/driver/UI theo. Không thể hứa port được nguyên nét mặt chỉ vì có shapekeys. Nếu chọn sẽ cần phiên bảnBlender riêng phù hợp và binary audit, không thay Blender đang dùng để giữ baseline cũ.

## 4. Quaternius Teen — bản tham chiếu ngân sách, không đề xuất art cuối

[Trang pack](https://quaternius.com/packs/universalbasecharacters.html) và [itch của tác giả](https://quaternius.itch.io/universal-base-characters) gắnCC0; mô tả humanoid retargetable, khoảng13ktris trung bình. Đây là số publisher, **chưa đo selected Teen mesh**. Chưa xác nhận facial morph/eye closure hoặc actual draw calls.

Preview đã tải cho thấy gương mặt/chất tạo hình trưởng thành/góc cạnh hơn mục tiêu BUM. Không dùng bodyadult/Superhero thu nhỏ hoặc recolor để gọi là BUM. Standard miễn phí cóglTF/FBX, import vào Blender vẫn chỉnh mesh/skin được; Source nguyên bản`.blend` và tiện ích niêm yết$19.99 lúc kiểm. Chưa mua.122MB/600MB là kích thước pack, không phải một character GLB hay runtime memory.

## Quy trình Codex + Blender đề xuất sau khi owner chọn

1. Pin nguồn/version/hash, đối chiếu grant và embedded notices; tách asset license khỏi add-on code. Không overwrite bản donor gốc hoặc C/P2/P3.1/P3.1R.
2. Tạo bản nghiên cứu riêng; audit mesh/UV/normals/skin, xác định mặt/hair/gloves/outfit cần thay. Không tự coi bone names/pose library là clips chạy game.
3. Giữ tạo hình trẻ em, tái thiết kế kit vàng07/navy và giày; tránh thao tác scale/recolor người lớn. VớiScott cần xử lý rig skin/export warnings và tạo facial runtime mapping có kiểm chứng.
4. Bake deform/constraints/morph cần thiết thành dữ liệu glTF thực hỗ trợ; không bake mất facial topology hoặc loại influence không đo lỗi. Không áp decimate toàn đầu chỉ để chốt budget.
5. Tái chạy Blink đủ5mức/2góc, Smile3mức, triangle-eye contact + ID visibility. **Blink của donor chưa được nghiệm thu dù P3.1R đã đạt**.
6. Xuất5góc matched studio; chỉ sau review mới đề xuất tích hợp game. Không thực hiện bước3–6 để tạo BUM donor trong lượt khảo sát này.

## iPhone và budgets

Đã có static WebKit WPE/Linux củaScott, chưa có Safari iPhone thật. PBR atlas/geometry file gọn hơn P3.1R không chứng minh FPS, heat, GPU memory hoặc animation cost.370joint palette không tự kết luận lỗi/hỗ trợ: cần đo weighted rig, bone-texture update, texture residency và multiplayer scene thực trên máy.

VớiSpring/Storm/Quaternius chưa có GLB kiểm riêng nên các chỉ số là`null`, không ước đoán thành số đo. Khi có donor được chọn, chốt budget từ asset bake thật và đo draw calls, texture memory, file size và thiết bị, không dùng native`.blend`/ZIP pack size làm runtime budget.

## Truy cập bị chặn / những gì chưa thể xác nhận

- Tool đọc trangStudio trả402, HTTP trực tiếp trả403 choSpring/Rain/Storm/remixing và thumbnail công khai. Nội dung publisher trong dossier được đối chiếu qua indexed primary-source text; registry license đọcHTTP200 trực tiếp. Không khẳng định đã mở Studio binary hoặc có local preview Studio.
- Wikimedia posterSpring và các trang này cũng trả403 qua downloader; không dùng poster không tải được làm ảnh đã kiểm. Link preview publisher giữ nguyên cho người dùng mở trực tiếp.
- Storm còn có subscription gate và yêu cầuBlender mới. Chưa chi tiền, chưa bypass; cần hợp pháp có file trước khi kiểm binary.
- Không có native source Quaternius miễn phí được audit. Không tự gọi Source trả phí là free hoặc mua rồi phân phối khi chưa chốt.

Dừng ở dossier lựa chọn asset. PR#2 vẫnDraft; main/Pages/Supabase và ba nhân vật khác không đổi. Không thuê artist, không tạo donor BUM và không thay model game trước khi chủ dự án duyệt.
