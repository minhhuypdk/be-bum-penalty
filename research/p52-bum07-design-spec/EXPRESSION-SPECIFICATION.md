# P5.2 — Expression Specification

8 trạng thái, mỗi trạng thái có PNG0° và45°. Neutral0° dùng cùng tệp ảnh với cận mặt turnaround để không tạo hai neutral khác nhau. Tất cả là ảnh AI concept, không phải ảnh từ cùng một mesh/rig/camera thật.

| Trạng thái | Mắt/mí/mày | Miệng/má/răng | Phân biệt với trạng thái khác |
|---|---|---|---|
| Neutral |Mắt hạnh nhân mở tự nhiên, mày nghỉ |Môi đóng mềm, không thấy răng, má không nâng chủ ý |Mốc nhận diện và số đo đầu; không dùng một nụ cười lớn làm rest |
| Happy |Mí mềm hơn, iris rõ; mày thả |Khóe/má nâng nhẹ, môi hé, chỉ cung răng trên |Không mở hàm nhưBigSmile; không nheo quá nhiều |
| Big Smile |Mí dưới nhấc theo má, iris vẫn rõ |Cười rộng, hàm mở vừa, cung răng trên và một phần răng dưới |Không thay sọ/hàm thành người khác, không dải răng trắng phẳng |
| Blink100 |Hai mí đóng kín, mày vẫn neutral |Má và miệng giữ neutral |Thiết kế mí đóng, không phải buồn ngủ/cười, không phải bằng chứng hết xuyên globe |
| Focused |Mày trong hạ/thu nhẹ, mắt hẹp vừa nhưng rõ iris |Môi đóng, má thả |Tập trung trước sút; ảnh hiện hơi nghiêm, cần duyệt cường độ |
| Surprised |Mày nâng, mí trên mở; kích thướcglobe/iris không được đổi ởmodel |MiệngO, hàm hạ nhẹ, răng phần lớn bị môi che |Ngạc nhiên thân thiện, không hoảng sợ hoặc mắt bật khỏisocket |
| Disappointed |Đầu mày trong nâng, mí thả nhẹ |Khóe môi hạ, môi đóng, má thả |Buồn nhẹ khi sút hụt, không khóc/bi kịch; giữ hướng đầu cố định |
| Celebration |Mày nâng hơn, má nhấc, mắt cười hẹp còn thấy một phầniris |Cười reo, hàm mở hơn, răng trên/dưới và ít lưỡi |KhácBigSmile bằng phối hợpmày–má–mí, không đổi sangpose ngửa đầu hoặc thêm tay |

## Các quan hệ cấu trúc bắt buộc sau khi được phép dựng

Globe giữ tâm/bán kính; mí đi trên bề mặt cầu và khóe mắt có mô liên tục. Smile có nâng khối má dẫn theo mí dưới, không chỉ kéo khóe miệng ngang. Jaw mở mang theo cằm/răng dưới/lưỡi; sọ và cung răng trên không đổi. Các răng nhìn ít/nhiều theo góc và độ hé môi, không sinh răng mới hoặc đổi cỡ răng giữa hai ảnh. Neutral, Blink, Focused và Disappointed không để lộ răng.

Ảnh hiện là đích thị giác, không phải bộkey biến dạng. Chưa cóAU/blendshape, topology, collision, mắt–mí contact, skin influences hoặc thử kết hợpBlink+Smile. Không dùng ảnh này hoặc kết quảP4.1R để ghiPASS kỹ thuật choP5.2.

## Những khác biệt phải chốt

Biên mí, nếp má, tooth silhouettes và độ rộng môi thay đổi nhẹ giữa hai góc. Bảng ảnh chưa đủ chứng minh một cung răng hoặc hairline duy nhất trong3D. Cường độFocused có thể đọc thành cau mày; Celebration có thể cần giảm độ nheo theo phản hồi chủ dự án. Xem `CONSISTENCY-REPORT.md` và `ACCEPTANCE-CHECKLIST.md`.
