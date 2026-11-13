# P4 — ma trận quyền sử dụng và ghi công

Kiểm ngày13/11/2026 (Asia/Saigon). Đây là kiểm chứng grant từ nguồn phát hành, không bảo đảm mọi thành phần của binary chưa tải. Không áp giấy phép Blender phần mềm cho tất cả model, không coi miễn phí=public domain.

| Asset | Chứng cứ gắn license với đúng asset | Game, gồm thương mại | Sửa | Phân phối `.glb` / geometry`.blend` | Điều kiện |
| --- | --- | --- | --- | --- | --- |
| Scott của **Mish7913/3DMish** | [Bài tác giả](https://blenderartists.org/t/boy-scott-free-3d-character-mish7913/1510925) dẫn [BY4.0](https://creativecommons.org/licenses/by/4.0/) và đúng [file gốc](https://projects.blender.org/3DMish/M7s-Assets-Library/raw/branch/main/data/characters/scott-3d-model.blend); HTTP200 đã tải | Có | Có | Có | Credit tác giả, link nguồn/license, nêu thay đổi; không gợi ý tác giả bảo trợ game; không thêm hạn chế làm mất quyền với asset. |
| Spring v1 | [Trang rig](https://studio.blender.org/characters/spring/v1/) được search index nguồn chính thức ghiCC-BY; [registry của publisher](https://projects.blender.org/studio/blender-studio/raw/branch/main/static_assets/fixtures/licenses.json) ghi slug`cc-by`→[BY4.0](https://creativecommons.org/licenses/by/4.0/). | Có theo grant này | Có | Có với phần được cấp BY4.0 | Credit`Spring Rig (CC-BY) Blender Foundation \| studio.blender.org`, link license/source, nêu thay đổi. Binary/notices/add-ons chưa kiểm; không đưa vào dự án lúc này. |
| Storm v1 | [Trang rig](https://studio.blender.org/characters/storm/v1/) gắnCC-BY; cùng registry publisherBY4.0. Access có phí tách biệt license. | Có theo grant này | Có | Có với phần được cấp BY4.0 | Credit`Storm Rig (CC) Blender Foundation \| studio.blender.org`, link license/source, nêu thay đổi. Chưa có binary và chưa mua subscription. |
| Quaternius Universal Base Characters | [Pack chính thức](https://quaternius.com/packs/universalbasecharacters.html) và [itch của tác giả](https://quaternius.itch.io/universal-base-characters) đều gắn [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/). | Có | Có | Có | Credit không bắt buộc theoCC0; vẫn lưu provenance. Free Standard không bao gồm mọi tiện ích của paid Source. |

Quyền ở bảng là quyền theo grant asset, không phải xác nhận mọi embedded code/add-on/material bên thứ ba của một binary chưa mở. Không đưa Spring/Storm vào model pipeline trước bước soát file đó. Ảnh publisher links không phải bằng chứng file đã được tải hay GLB đã chạy.

## Cách áp dụng đúng khi tích hợp sau này

- CC BY4.0 cho phép share/adapt kể cả thương mại; cần attribution, link license và nêu thay đổi. Không phải ShareAlike và không tự buộc toàn bộ game mở mã. Giữ nguyên license/credit của phần donor thay vì gắn nhãn mesh hoàn toàn tự tạo.
- Native rig có thể chứa Python/add-on GPL hoặc thành phần có notices riêng. Giữ/tôn trọng license code tương ứng nếu phân phối code/source, không mặc nhiên gộp code vào CC-BY. GLB không mang UI/driver Python theo.
- WebGL/GitHub Pages phục vụ asset có thể tải về; repo công khai chứa raw GLB. Vì vậy cần quyền phân phối, không chỉ quyền render video. Không tự đưa model Royalty-Free/no-redistribution, Editorial, NC hoặc ND vào repo này.
- Không dùng fan-art franchise chỉ vì uploader ghiCC0. Scott trong hồ sơ là tác phẩm củaMish7913, **không phải** model Scott khác củaMakar Malicki; không tráo nguồn hoặc license giữa các asset trùng tên.
- Không mua asset/source/subscription và không dùng bản tải vượt paywall. HTTP403/402 chỉ nói truy cập bị chặn, không thay grant pháp lý hoặc quyền tải.

## Credit dự kiến nếu donor được chọn

Scott: `Boy (Scott) by Mish7913 / 3DMish — CC BY4.0 — <author source> — modified: [ghi cụ thể thay đổi sau này].` Hiện chỉ có unmodified-geometry GLB static probe, không phải BUM adaptation.

Spring/Storm: giữ credit publisher tương ứng ở bảng, thêm link license, nguồn đúng phiên bản và changelog kit/geometry/rig sau này. Không tuyên bố Foundation hỗ trợ hay nghiệm thu BÉ BUM.

Nguồn pháp lý: [CC BY4.0 deed/legal code](https://creativecommons.org/licenses/by/4.0/), [CC0 deed](https://creativecommons.org/publicdomain/zero/1.0/). `evidence/studio-license-mapping.json` lưu bản ghiCC-BY đã đọc trực tiếp và hash nguồn registry.
