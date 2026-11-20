# P5.4 — Base mesh, nguồn và giấy phép

Kiểm ngày20/11/2026. Ưu tiên miễn phí, sửa và phân phối được trong game/repo công khai. Dưới đây có base trẻ em/chibi, một nhân vật phim trẻ em và base topology chung có preset trẻ em; **không gọi tất cả là nhân vật trẻ em hoàn thiện**. Không mua Source/subscription, không dùng nguồn reupload hoặc fan-art không rõ quyền.

## 1. Head – Generic Topology — Paul Kotelevets / Blender Human Base Meshes v1.4.1

- [Trang phát hành chính thức](https://www.blender.org/download/demo-files/), [ZIP chính thức đã tải](https://download.blender.org/demo/asset-bundles/human-base-meshes/human-base-meshes-bundle-v1.4.1.zip), [CC0](https://creativecommons.org/publicdomain/zero/1.0/). Dùng asset **đúng tên `Head - Generic Topology`**, không thay bằng Snow/Rain/Scott.
- **Binary đã mở chỉ đọc.** 318 vertex, 316 quad, 632 base triangle; UVMap; Subsurf viewport1. Chín design keys ngoài Basis: có `Real_Kid`, `Toon_Anime_Kid`, các ví dụ người lớn/animal khác. Đây **không phải** Blink/Smile; asset không có armature. Không chạy preset, không tạo bản BUM trong P5.4.
- Bằng chứng quyền: metadata đúng object ghi tác giả Paul Kotelevets, license CC0; README bundle ghi mọi asset được cung cấp là CC0. Native còn text `License` nói **Rain Rig CC BY4.0**; giữ nguyên trong chứng cứ, không xóa/giả vờ không tồn tại. Câu này cấp phép Rain Rig, không tự chuyển Head Generic sang BY và không cho phép gọi Rain Rig là CC0. Phạm vi đề xuất chỉ Head Generic đã có grant CC0 riêng; nếu lấy thêm mesh/material/code thì kiểm riêng. Không tái phân phối nguyên bundle trong repo P5.4.
- **Phù hợp B:** hữu ích cho sculpt thủ công oval trẻ em và định hình mắt/mũi/môi bằng cage; child design key chứng minh có biến thể thiết kế, không chứng minh khớp B. Chỉ có đầu nên chưa có tỷ lệ toàn thân5H; chưa có tóc rẽ lệch, iris/vật liệu cuối hoặc cung răng BUM. Preset anime không được mặc nhiên dùng làm ngoại hình B.
- **Việc còn cần:** sculpt hình khối thật theo B, bổ sung chi tiết mí/môi/khóe/mouth interior, mắt và tóc; kiểm/sửa loops sau biến dạng lớn, UV/bake và facial rig. UV có sẵn không đồng nghĩa unwrap cuối không méo. Dễ thử cage hơn R, không bảo đảm ít giờ mỹ thuật hơn.
- **Quyền:** dùng thương mại, sửa, phân phối mesh/GLB/blend theo CC0; credit không bắt buộc, nên lưu `Head – Generic Topology — Paul Kotelevets / Blender Human Base Meshes v1.4.1 — CC0`, URL/hash/changelog. Không suy quyền với code/add-on riêng.
- **Xếp loại:** ứng viên kỹ thuật ưu tiên cho hướng B, **chưa nghiệm thu ngoại hình**. Có thể dùng đúng phần CC0 nếu chủ dự án chọn; chưa append vào model dự án.

## 2. Tiby — PINKCANNON

- [Bài phát hành tác giả trên OpenGameArt](https://opengameart.org/content/tiby-3d-rigged-model), [ZIP gốc đã tải](https://opengameart.org/sites/default/files/Tiby_Character_MnF_0.zip), [CC0](https://creativecommons.org/publicdomain/zero/1.0/), [preview chính chủ](https://opengameart.org/sites/default/files/Display_Tiby.png).
- **Binary nam `TIBY.blend` đã mở chỉ đọc**, chưa kiểm binary nữ trong ZIP. 25 bones,16 deform,4 constraints; body max4 vertex groups có weight>1e-6, 0 vertex vượt4 trong phép đo native. Không có shape keys; chưa test chuyển động hay GLB.
- Body đo được1,784tri, hair616tri = **2,400tri**; publisher ghi body1,794tri, nên lưu cả hai số, không sửa báo cáo cho giống quảng cáo. Scene tổng3,424tri còn Sphere/Circle là custom-shape rig đã xác nhận qua pose bone references; không cộng chúng vào budget thân/tóc. Body/hair có UV, raw manifold. Đây là số viewport evaluated trong Blender4.3.2, không là game draw calls.
- **Phù hợp B:** chibi/toon có nét trẻ, nhưng preview mặt rất đơn giản, thiếu mắt hạnh nhân/mũi/môi sculpt; đầu lớn và tóc xanh dạng khối che mặt. Không có phép đo5H. Tóc, face và tỷ lệ phải làm lại sâu, không chỉ recolor.
- **Việc còn cần:** facial structure/loops/mouth interior/teeth hoàn toàn mới; tóc mới; sửa tỷ lệ theo5H rồi skin lại/kiểm rig. Số poly thấp giúp kỹ thuật, không đạt mỹ thuật mong muốn chỉ bằng Subsurf.
- **Quyền:** CC0 từ đúng entry và author; game thương mại/sửa/rawGLB/blend được; không bắt buộc credit, khuyến nghị PINKCANNON + nguồn/license + thay đổi.
- **Xếp loại:** hợp lệ để thử kỹ thuật, **không khuyến nghị làm mặt BUM** vì khối mặt hiện có quá sơ lược.

## 3. Boy — Lula Borges / BlendSwap5024

- [Entry đúng asset](https://blendswap.com/blend/5024), [preview chính chủ](https://img.blendswap.com/archive/images/2012/04/blend_41773/lula_borges_boy_big_3777c06ac6df3a1cd996b46818b47df037d8c920.jpg), [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
- Trang hiện tại ghi CC0, tác giả Lula Borges, rigged low-poly boy, chưa texture; Blender2.6x/Blender Internal. **Chưa tải/mở binary.** Rig, facial controls, topology/UV, influences, blendshape count và GLB đều chưa được đo; comment người dùng không được dùng thay audit.
- **Phù hợp B qua preview:** là bé trai, tóc ngắn quét lệch tương đối gần ý đồ. Tuy nhiên mắt tròn xanh/lồi, mặt tròn và khối môi–mũi kiểu cũ; khác oval/mắt hạnh nhân/nâu của B. Không đo5H từ ảnh phối cảnh. Chiều ngôi tóc phải kiểm lại theo trái giải phẫu, không suy từ ảnh có thể mirror.
- **Việc còn cần:** mở ở Blender phù hợp, kiểm chuyển đổi legacy materials/constraints, resculpt face/eyelids, tóc và kit07; retopo/UV/facial rig nếu binary không đáp ứng. Chưa có bằng chứng bỏ được các việc này.
- **Quyền:** CC0 hiển thị trên đúng entry, cho game/sửa/phân phối, credit tự nguyện. Khi lấy binary cần lưu hash/notices và xác nhận đúng asset, không dùng link “similar assets” có BY-SA/NC khác.
- **Xếp loại:** ứng viên trẻ em hợp pháp nhưng rủi ro legacy và thẩm mỹ; chưa ưu tiên hơn R/Head Generic.

## 4. Spring v1 — Blender Foundation / Blender Studio

- [Trang rig chính thức](https://studio.blender.org/characters/spring/v1/), [CC BY4.0](https://creativecommons.org/licenses/by/4.0/), [registry license của publisher](https://projects.blender.org/studio/blender-studio/raw/branch/main/static_assets/fixtures/licenses.json). Trang đã đọc trực tiếp HTTP200 dù web search open từng trả402; không coi lỗi tool là phải mua quyền.
- Trang ghi Free, Blender2.8–3.6 và BlenRig; native download≈406.5MB. **Chưa tải binary/add-on hoặc mua subscription.** Preview chính chủ đã xem: có facial/body controls, nhưng chưa đo joints/skin/shape keys hoặc GLB.
- **Phù hợp B:** độ mềm và hoàn thiện khuôn mặt/hair của nhân vật phim hữu ích hơn các base low-poly trong việc tham chiếu. Tuy nhiên đây là cô bé Spring với nhận diện riêng, mắt xanh tròn, tóc/trang phục khác; không phải BUM nam và không được dùng nguyên mặt chỉ đổi áo. Tỷ lệ5H chưa đo.
- **Việc còn cần:** resculpt nhận diện B, tóc ngắn rẽ trái, kit; đọc topology, modifiers/drivers, kiểm bản Blender/BlenRig tương thích; facial/body rig cần bake hoặc chuyển sang export rig có test tương đương. Shader/hair kiểu phim không tự đi sang WebGL; cần hair mesh/bake PBR/UV và tối ưu sau duyệt.
- **Quyền:** share/adapt kể cả thương mại theo BY4.0; GLB/blend được phân phối nếu credit, URL nguồn/license, nêu thay đổi, không ngụ ý bảo trợ và không thêm hạn chế trái license. Credit publisher yêu cầu: `Spring Rig (CC-BY) Blender Foundation | studio.blender.org`; thêm bản chỉnh sửa BUM cụ thể khi có. Code/BlenRig có thể có license khác, không gộp vào BY.
- **Xếp loại:** tham chiếu sculpt/rig và ứng viên thích nghi có điều kiện; rủi ro đổi nhận diện/rig cao, không là đường tắt miễn phí tới9/10.

## 5. Universal Base Characters — Quaternius, biến thể Teen cần kiểm

- [Trang tác giả](https://quaternius.com/packs/universalbasecharacters.html), [itch của tác giả](https://quaternius.itch.io/universal-base-characters), [CC0](https://creativecommons.org/publicdomain/zero/1.0/), [preview lịch sử đã có](../p4-character-assets/previews/quaternius-preview.jpg).
- Publisher ghi6base (male/female Superhero/Regular/Teen), Humanoid rig, hair options, average13ktri; đó là **claim của publisher, chưa là số đo P5.4**. Chưa tải Standard và chưa xác nhận đúng Teen male/hairstyle nào trong bản miễn phí. Source có .blend/tiện ích riêng và đang ghi$19.99; không mua. Có thể chỉnh mesh glTF/FBX miễn phí trong Blender nếu đúng biến thể được cung cấp, không bắt buộc mua Source để sửa geometry.
- **Phù hợp B:** Teen gần trẻ hơn Superhero/Regular, nhưng không phải bé trai5H sẵn; mặt/mắt/mũi/môi và tóc cần sculpt lớn. Không dùng cách thu nhỏ người lớn. Không xác nhận tóc rẽ trái/mái thấp trong Standard.
- **Việc còn cần:** audit selected free file, facial loops/UV/morphs/influences; đổi tỷ lệ theo giải phẫu trẻ, resculpt hair/face, kit07 và kiểm skin sau thay đổi. Rig body Humanoid không chứng minh có facial rig hoặc Blink.
- **Quyền:** CC0 của đúng pack cho game/sửa/phân phối; credit tự nguyện. License không đồng nghĩa mọi file trả phí được tải miễn phí; chỉ lấy Standard hợp lệ nếu được chọn. Không mua/subscription trong P5.4.
- **Xếp loại:** phương án dự phòng thiên về kỹ thuật game; không ưu tiên tạo hình BUM.

## Ma trận pháp lý

| Asset / phạm vi | Game thương mại | Sửa | Phân phối rawGLB/blend | Credit | Mức chứng cứ |
|---|---|---|---|---|---|
| Head Generic đúng object | Có, CC0 | Có | Có với phần CC0 đã xác định | Tự nguyện | Metadata + README native gốc; giữ text Rain riêng, không mở rộng grant |
| Tiby, file nam đã kiểm | Có, CC0 | Có | Có | Tự nguyện | Entry chính chủ + hash ZIP/native |
| Boy5024 | Có theo entry CC0 | Có | Có theo grant | Tự nguyện | Trang/preview đã đọc; binary notices chưa kiểm |
| Spring v1 | Có, BY4.0 | Có | Có với credit/changelog | Bắt buộc | Trang link trực tiếp BY4.0 + publisher registry; binary chưa kiểm |
| Quaternius Standard đúng file | Có, CC0 | Có | Có | Tự nguyện | Hai trang tác giả; binary/biến thể miễn phí chưa kiểm |

CC0 không xóa quyền nhãn hiệu/nhân thân của bên khác; BY4 không bắt cả game đổi license nhưng phải bảo toàn điều kiện của phần được cấp. Không chọn fan-art, NC, ND, Editorial hoặc EULA không cho raw asset trong repo công khai. Không suy license của software Blender/GPL thành license của model. Các điều kiện trên là phạm vi grant đọc được, không bảo đảm phần bên thứ ba chưa mở.

**Không asset nào được tuyên bố khớp B hoặc đạt9/10.** Danh sách này cho phép chủ dự án chọn đầu vào kiểm tiếp; không phải nghiệm thu mô hình thay thế.
