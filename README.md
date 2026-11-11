# BÉ BUM PENALTY 3D

Game luân lưu gia đình cho hai thiết bị: một người chọn **BA**, người còn lại chọn
**BUM**. Trạng thái trận đấu đồng bộ qua Supabase Realtime, có polling dự phòng.

Game đang phát hành: https://minhhuypdk.github.io/be-bum-penalty/

Mở cùng link trên hai iPhone, chọn hai vai khác nhau, rồi chọn hướng sút/bắt.
Sau kết quả, chạm **Lượt tiếp**. Mỗi thiết bị chỉ nên mở một phiên cùng vai.
Trang Pages phục vụ nhánh `main`; nhánh phát triển có thể có đồ họa chưa phát hành.

## Chạy và kiểm thử

Game là website tĩnh, không cần build hoặc đổi database để chạy đồ họa.
Dùng `python3 -m http.server 4173` để mở tại `http://localhost:4173`.

Bộ kiểm thử yêu cầu Node.js 20+, curl và Chromium/Playwright:

```sh
npm ci
npx playwright install chromium
npm test
```

`npm test` tự mở máy chủ localhost ở cổng trống, kiểm tra luật, sân, bốn nhân vật,
âm thanh và hai phiên đồng thời với REST mô phỏng. Không ghi Supabase thật.
Ảnh kiểm thử lưu trong `artifacts/` (không commit). Có thể đặt `CHROMIUM_PATH`
nếu Chromium đã có trên máy ở một đường dẫn riêng.

`npm run test:live` dùng Supabase thật, tạo duy nhất một phòng `graphics-test-*`
riêng, tắt polling để kiểm tra Realtime, rồi trả vai đã chiếm. Không xóa dữ liệu
hoặc dùng phòng gia đình `ba-bum`; dòng kiểm thử được giữ lại. Công cụ cloud hiện
chuyển REST qua curl để sử dụng proxy tin cậy; WebSocket Realtime vẫn được dùng.

## Phát hành và khôi phục

Chỉ merge sau khi các kiểm thử đạt. GitHub Pages hiện lấy `main`, thư mục `/`.
Nhánh `backup/2d-compatible` giữ giao diện 2D cùng các sửa lỗi kết nối đã kiểm thử.
Bản nguyên gốc vẫn ở `backup/pre-3d-b9e188f`. Có thể chọn nhánh tương thích trong
Settings → Pages để khôi phục, hoặc revert merge bằng PR mới mà không viết lại
lịch sử. Xem [hướng dẫn phát hành](docs/RELEASE-CHECKLIST.md).

## Đồ họa đang phát triển

[Xưởng nhân vật](graphics/review.html) cho phép duyệt bốn biến thể và chuyển động,
không truy cập Supabase. [Hướng mỹ thuật](docs/ART-DIRECTION.md) và
[module sân/âm thanh](docs/STADIUM-AUDIO.md) ghi rõ kết quả và giới hạn.
Chất lượng hoạt hình điện ảnh cao cấp vẫn là mục tiêu đang hoàn thiện; mô hình
thủ tục hiện tại chưa được coi là tài sản cuối cùng. Safari/GPU và giọng hô tiếng
Việt trên iPhone thật vẫn cần kiểm tra trực tiếp.

## Kiểm thử và tiếp tục phiên (PR #2, chưa phát hành)

Bản phát triển chỉ lưu vai sau khi máy chủ xác nhận. Nếu rời vai thất bại do
mất mạng, máy vẫn giữ phiên để có thể thử lại. Phiên mới trên cùng thiết bị có
thể dùng nút “Tiếp tục BA/BUM trên máy này” khi còn dấu phiên hợp lệ; trận và tỷ
số được giữ nguyên, phiên cũ không còn điều khiển vai đó. Không tự thu hồi vai
của thiết bị khác. Phiên cũ trước bản mới hoặc mất localStorage không tự phục hồi.

`npm run test:live` hiện bao gồm cả tranh vai đồng thời, từ chối vai đã chiếm,
rời vai khi lỗi mạng, thử lại, tải lại, chuyển phiên và chặn phiên cũ. Chỉ dùng
phòng kiểm thử riêng; không đổi quyền, RLS, schema hoặc dữ liệu gia đình.

PR #2 giữ ở dạng draft và chỉ merge sau khi chủ dự án đồng ý.

## Character Showcase riêng — PR #2 chưa merge

https://be-bum-character-showcase.jovialmesa21.chatgpt.site

Bản xem trước riêng cho tài khoản sở hữu, phiên bản 1. Đăng nhập ChatGPT của
chủ dự án để mở trên iPhone. Phòng trưng bày có bốn nhân vật, xoay/zoom/cận mặt,
năm chuyển động, PNG export, đo FPS và duyệt GLB cục bộ. Không kết nối Supabase.

Xem [báo cáo FPS](showcase/FPS-REPORT.md), [ảnh render](showcase/renders),
[quy trình asset hợp pháp](docs/SHOWCASE-ASSET-PIPELINE.md) và
[hồ sơ xuất bản](showcase/DEPLOYMENT.md). Số đo Linux phần mềm không phải FPS
iPhone; chất lượng so với ảnh mẫu vẫn cần đối chiếu vì ảnh không có trong
ngữ cảnh hiện tại. Main/game công khai và dữ liệu Supabase giữ nguyên.
