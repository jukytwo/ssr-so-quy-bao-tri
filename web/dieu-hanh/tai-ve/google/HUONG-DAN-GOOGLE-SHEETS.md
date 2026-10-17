# Hướng dẫn nối SSR Điều Hành với Google Sheets

## Cài đặt nhanh (khoảng 5 phút, chỉ một tệp)

Từ bản này, cổng cư dân và trang hiện trường đã nằm sẵn trong **Code.gs**, không phải tạo tệp Portal, Field riêng. Hai tệp Portal.html và Field.html chỉ để tham khảo.

| Bước | Làm gì |
|---|---|
| 1 | Đăng nhập tài khoản Google của Ban Quản lý, mở địa chỉ **sheets.new** để tạo bảng tính trống, đặt tên `SSR Dieu Hanh du lieu chung` |
| 2 | Menu **Tiện ích mở rộng**, chọn **Apps Script**. Xóa hết mã mẫu, dán toàn bộ nội dung **Code.gs**, bấm lưu |
| 3 | Bấm **Triển khai**, **Tùy chọn triển khai mới**, bánh răng chọn **Ứng dụng web**. Thực thi với tư cách: **Tôi**. Người có quyền truy cập: **Bất kỳ ai**. Bấm **Triển khai**. Nếu Google hỏi quyền: chọn tài khoản, **Nâng cao**, **Đi tới dự án**, **Cho phép** (cảnh báo "chưa xác minh" là bình thường vì đây là tập lệnh của chính Ban Quản lý) |
| 4 | Quay lại trình soạn mã, chọn hàm `caiDat`, bấm **Chạy** (cho phép quyền nếu được hỏi). Hàm tự tạo các trang dữ liệu, cài lịch tự động và **gửi email cho chính tài khoản này** một **Chuỗi kết nối** (bắt đầu bằng `SSRDH|`), đường dẫn cổng cư dân, trang hiện trường, khóa xem và mã hiện trường |
| 5 | Mở file **SSR-DieuHanh-offline.html**, vào **Cài đặt và dữ liệu**, bấm **Xóa dữ liệu mẫu**; rồi ở mục **Dữ liệu chung qua Google Sheets**, dán nguyên Chuỗi kết nối vào ô địa chỉ, bấm **Lưu và kiểm tra** |

Email cảnh báo mặc định gửi về chính tài khoản đã cài. Muốn thêm người nhận, xem Bước 2 bên dưới (thuộc tính `NOTIFY_EMAIL`, `BQT_EMAILS`). Chạy lại hàm `chuoiKetNoi` bất cứ lúc nào để nhận lại email thông tin kết nối.

Trang hiện trường cho bảo vệ, kỹ thuật báo sự cố cắt nước, điện: địa chỉ web app thêm `?sc=1` ở cuối.

---

## Cài đặt đầy đủ (cách cũ, vẫn dùng được)

**Quan trọng:** SSR Điều Hành dùng một bảng tính và một bản triển khai **riêng**, không dùng chung với công cụ quản lý cũ hay công cụ Theo dõi phản ánh. Máy chủ bản này chỉ nhận dữ liệu của SSR Điều Hành, nên hai công cụ không thể ghi đè lên nhau.

Làm một lần, khoảng 20 đến 25 phút, trên máy tính đăng nhập tài khoản Google của Ban Quản lý. Xong sẽ có:

| Thành phần | Dùng để làm gì |
|---|---|
| Bảng tính "SSR Dieu Hanh du lieu chung" | Kho dữ liệu chung; mỗi phân hệ là một sheet chỉ xem (Tổng quan có biểu đồ, Cảnh báo, Phản ánh, Bảo trì, Thu chi, Công nợ...) |
| Địa chỉ web app `/exec` | Vừa là cổng cư dân (in mã QR dán sảnh), vừa là máy chủ cho công cụ quản lý |
| Khóa quản trị và khóa xem | Khóa quản trị để sửa dữ liệu, khóa xem cho Ban Quản trị và nhân viên chỉ xem |
| Email tự động | Cảnh báo mỗi giờ khi có việc lên mức Cảnh báo hoặc Khẩn cấp; bản tin 7 giờ sáng kèm PDF |
| Sao lưu | Mỗi đêm chép dữ liệu vào thư mục "SSRDH sao luu", giữ 30 ngày |
| Trang hiện trường | Bảo vệ, kỹ thuật quét mã QR dán tại điểm tuần tra, thiết bị, công tơ, và mã khách của cư dân |
| Cổng cư dân mở rộng | Cư dân xem phí và quét VietQR, tự đặt tiện ích, đăng ký khách trước, gửi ảnh kèm phản ánh |

## Bước 1. Tạo bảng tính và dán mã

1. Vào Google Drive, tạo một Google Sheets mới, đặt tên `SSR Dieu Hanh du lieu chung`.
2. Chọn menu **Tiện ích mở rộng**, rồi **Apps Script**.
3. Xóa mã mẫu trong tệp `Mã.gs`, dán toàn bộ nội dung file **Code.gs**.
4. Bấm dấu **+** cạnh mục Tệp, chọn **HTML**, đặt tên đúng là `Portal`, xóa nội dung mẫu, dán toàn bộ file **Portal.html**.
5. Làm tương tự, tạo tệp HTML thứ hai tên đúng là `Field`, dán toàn bộ file **Field.html**.
6. Bấm biểu tượng lưu.

## Bước 2. Khai báo email nhận thông báo

Trong Apps Script, bấm **Cài đặt dự án** (biểu tượng bánh răng bên trái), kéo xuống mục **Thuộc tính tập lệnh**, bấm **Thêm thuộc tính tập lệnh**:

| Thuộc tính | Giá trị | Nhận gì |
|---|---|---|
| `NOTIFY_EMAIL` | Email của Ban Quản lý, nhiều email cách nhau bằng dấu phẩy | Cảnh báo mỗi giờ, tin cư dân mới, bản tin sáng |
| `BQT_EMAILS` | Email các thành viên Ban Quản trị | Chỉ bản tin sáng 7 giờ |

## Bước 3. Chạy cài đặt

1. Quay lại trình soạn mã, chọn hàm `caiDat` ở thanh công cụ, bấm **Chạy**.
2. Google hỏi quyền: chọn tài khoản Ban Quản lý, bấm **Nâng cao**, **Đi tới dự án**, **Cho phép**. Cảnh báo "chưa xác minh" là bình thường vì đây là tập lệnh của chính Ban Quản lý.
3. Mở **Nhật ký thực thi** bên dưới, chép lại **Khóa quản trị** (bắt đầu `QT-`), **Khóa xem** (bắt đầu `XEM-`) và **Mã hiện trường** (6 chữ số, đưa cho bảo vệ và kỹ thuật).

Hàm `caiDat` tạo các sheet, sinh khóa và cài ba lịch tự động. Chạy lại lần nữa không bị trùng lịch.

## Bước 4. Triển khai thành web app

1. Bấm **Triển khai**, chọn **Tùy chọn triển khai mới**, bấm bánh răng, chọn **Ứng dụng web**.
2. **Thực thi với tư cách**: chọn **Tôi**. **Người có quyền truy cập**: chọn **Bất kỳ ai**.
3. Bấm **Triển khai**, chép địa chỉ dạng `https://script.google.com/macros/s/.../exec`.

"Bất kỳ ai" để cư dân mở cổng mà không cần tài khoản Google. Muốn xem hộp thư hay dữ liệu vận hành vẫn bắt buộc phải có khóa.

## Bước 5. Tự kiểm tra

Chọn hàm `kiemTra`, bấm **Chạy**, xem Nhật ký thực thi. Mọi dòng phải là **ĐẠT**. Hàm này gửi một tin thử, đánh dấu đã đọc, phản hồi, rồi xóa tin thử; kiểm tra quyền ghi Drive, lịch tự động và email. Dòng nào **LỖI**, anh chụp màn hình gửi lại.

Tải lại trang bảng tính sẽ thấy menu **SSR Điều Hành** trên thanh công cụ, có các lệnh: cập nhật bảng, gửi cảnh báo, gửi bản tin sáng, sao lưu, kiểm tra hệ thống, xem khóa.

## Bước 6. Kết nối công cụ quản lý

1. Mở **SSR-DieuHanh-offline.html** bằng Chrome, Edge hoặc Safari trên máy tính.
2. Vào **Cài đặt và dữ liệu**, mục **Dữ liệu chung qua Google Sheets**, dán địa chỉ web app và khóa quản trị, bấm **Lưu và kiểm tra**.
3. Đăng nhập quản trị, bấm **Đẩy bản này lên**. Khoảng nửa phút sau, bảng tính có đủ các sheet phân hệ.

Máy khác làm tương tự với khóa của mình. Mỗi lần lưu, dữ liệu tự đẩy lên sau vài giây. Các sheet trong Google Sheets cập nhật tối đa 5 phút một lần; muốn cập nhật ngay thì bấm **Cập nhật Google Sheets ngay** trong Cài đặt. Mỗi lúc chỉ một người được sửa dữ liệu chung; quyền sửa tự nhả khi người đó thoát quản trị hoặc sau 10 phút không hoạt động.

Trang công cụ đăng trên Claude không gọi được máy chủ Google do chính sách bảo mật của Claude, nên dùng file offline hoặc trang ở Bước 8.

## Bước 7. Cổng cư dân và chia sẻ bảng tính

- Địa chỉ web app chính là cổng cư dân. Trong công cụ, bấm **In áp phích QR cho cư dân** để in dán sảnh, thang máy.
- Tin cư dân hiện ở **Hộp thư cư dân**. Người quản trị mở tin là cư dân thấy dấu đã đọc. Chuyển thành phản ánh thì cư dân thấy đang xử lý; phản ánh xong thì tin tự sang đã xong.
- Chia sẻ bảng tính cho Ban Quản trị với quyền **Người xem**. Họ mở trên ứng dụng Google Sheets là thấy Tổng quan, Cảnh báo và từng phân hệ. Các sheet phân hệ đã khóa, chỉ chủ bảng tính sửa được, và mọi thay đổi phải làm trong công cụ để có nhật ký.

## Bước 8. Mã QR hiện trường và cổng cư dân mở rộng

- **In mã QR dán tại chỗ:** trong công cụ có nút **In mã QR** ở ba nơi: Vận hành và bảo trì, mục Hồ sơ thiết bị (dán ở thang máy, tủ điện, trạm bơm); mục Điện nước khu chung (dán cạnh công tơ); Hầm xe và ra vào, mục Tuần tra bảo vệ (dán tại từng điểm tuần tra). Nên in trên giấy decal chống nước.
- **Bảo vệ, kỹ thuật:** quét mã bằng camera điện thoại. Lần đầu nhập mã hiện trường và tên. Sau đó mỗi lượt chỉ cần bấm xác nhận, chọn tình trạng, chụp ảnh nếu cần. Thiết bị báo "Hỏng" sẽ tự tạo phản ánh khẩn cho kỹ thuật.
- **Đưa ghi nhận vào công cụ:** người quản trị mở công cụ khi đã kết nối là dữ liệu tự về sau vài phút: lượt tuần tra, ngày kiểm tra thiết bị, chỉ số công tơ, khách vào cổng. Có thể bấm **Làm mới** ở mục yêu cầu đặt chỗ để lấy ngay.
- **Cư dân:** giấy báo phí in từ công cụ có **mã tra cứu** 6 ký tự của từng căn. Cư dân dùng mã này trên cổng để xem phí, quét VietQR, tự đặt tiện ích và đăng ký khách. Ban Quản lý duyệt yêu cầu đặt chỗ trong mục Tiện ích và đặt chỗ; cư dân thấy kết quả ngay trên cổng.
- **Khách đăng ký trước:** cư dân gửi mã QR cho khách, bảo vệ quét mã ở cổng, hệ thống kiểm tra đúng ngày và khung giờ, ghi giờ vào, giờ ra vào nhật ký cổng.
- **Ảnh hiện trường:** lưu trong thư mục "SSRDH anh hien truong" trên Drive. Trong công cụ, mở phản ánh, việc bảo trì hoặc thiết bị rồi bấm **Ảnh hiện trường** để xem hoặc tải thêm ảnh trước, sau xử lý.

## Bước 9 (tùy chọn). Trang Ban Quản lý trên điện thoại

1. Tải **SSR-DieuHanh-offline.html** lên Drive của Ban Quản lý, không chia sẻ công khai.
2. Mở file trên Drive, chép mã tệp trong địa chỉ (đoạn giữa `/d/` và `/view`).
3. Thêm thuộc tính tập lệnh `BQL_FILE_ID` với giá trị là mã đó.
4. Nhân viên mở địa chỉ web app có thêm `?p=bql` ở cuối, vào Cài đặt nhập khóa một lần.

## Khi cập nhật mã

Vào **Triển khai**, chọn **Quản lý các bản triển khai**, bấm bút chì, chọn phiên bản mới rồi bấm **Triển khai**. Địa chỉ giữ nguyên, không phải in lại mã QR. Nếu mã mới có thêm lịch tự động, chạy lại `caiDat`.

## Lưu ý

- Bảng tính, thư mục sao lưu và các file `SSRDH-du-lieu-chung.json`, `SSRDH-bang-tinh.json` chứa thông tin cư dân: chỉ chia sẻ trong Ban Quản lý và Ban Quản trị, không để chế độ "Bất kỳ ai có đường liên kết".
- Nghi khóa bị lộ thì chạy hàm `doiKhoa`, rồi nhập khóa mới trên các máy. Muốn đổi mã hiện trường, xóa thuộc tính `GUARD_PIN` trong Thuộc tính tập lệnh rồi chạy lại `caiDat`.
- Muốn vô hiệu toàn bộ mã tra cứu cư dân (ví dụ bị lộ danh sách), vào công cụ, Cài đặt, bấm **Đổi toàn bộ mã tra cứu**, đồng bộ, rồi in lại giấy báo phí.
- Hạn mức miễn phí của Google đủ cho một khu chung cư: tài khoản Gmail thường gửi được khoảng 100 email mỗi ngày, Google Workspace nhiều hơn. Cảnh báo chỉ gửi khi có việc mới lên mức hoặc tăng mức, nên không bị lặp.

## Bước 10. Phiên bản, báo cáo tuần, Excel dữ liệu chung, chấm điểm của cư dân

Các tiện ích này có sẵn trong bản Code.gs hiện tại. Nếu đã cài bản trước, dán lại Code.gs và Portal.html, chạy lại `caiDat` một lần (để thêm lịch gửi báo cáo tuần và sheet DanhGia), rồi triển khai phiên bản mới.

| Tiện ích | Cách dùng |
|---|---|
| 60 phiên bản gần nhất | Mỗi lần đồng bộ, máy chủ chép một bản vào thư mục "SSRDH phien ban". Trong SSR Điều Hành: Cài đặt và dữ liệu, mục Excel và dữ liệu chung, **Xem phiên bản**, chọn **Khôi phục** và ghi lý do. Khôi phục tạo phiên bản mới, không xóa lịch sử. |
| Báo cáo tuần qua email | Sáng thứ Hai lúc 7 giờ, máy chủ gửi báo cáo tuần kèm PDF tới NOTIFY_EMAIL và BQT_EMAILS: việc quá hạn theo bốn mức, việc đã xong trong 7 ngày. |
| Excel dữ liệu chung | Trong SSR Điều Hành bấm **Lấy liên kết** để có bốn liên kết (Phản ánh, Kế hoạch, Nhật ký tiến độ, Lời nhắn). Trên Excel máy tính: Dữ liệu, Từ Web, dán từng liên kết vào ô A1 các trang Nguồn PA, Nguồn KH, Nguồn NK, Nguồn LN của file Saigon-South-Residences-Dashboard-van-hanh-du-lieu-chung.xlsx. Từ đó chỉ cần Dữ liệu, Làm mới tất cả. Liên kết chứa khóa xem, chỉ gửi Ban Quản lý, Ban Quản trị. |
| Tình hình vận hành công khai | Cổng cư dân có mục Tình hình vận hành: số phản ánh đang xử lý, việc quá hạn, việc xong trong 7 ngày và theo từng khu vực; không ghi tên hay căn hộ. |
| Chấm điểm hài lòng | Khi phản ánh gắn với tin nhắn của cư dân được hoàn thành, cư dân chấm từ 1 đến 5 sao trong mục Tin của tôi. Công cụ tự nhận điểm vào ô Đánh giá của cư dân của phản ánh, có ghi lịch sử. |
| Lời nhắn trong công cụ | Khi đã nối, lời nhắn viết trong SSR Điều Hành cũng được gửi thẳng vào Hộp thư cư dân trên máy chủ. |

## Bước 11. Tình trạng dịch vụ theo căn và khảo sát hài lòng

Bản Code.gs và Portal.html hiện tại có thêm hai tiện ích. Nếu đã cài bản trước: dán lại hai tệp, chạy lại `caiDat` một lần để tạo sheet KhaoSat, rồi triển khai phiên bản mới.

| Tiện ích | Cách dùng |
|---|---|
| Tình trạng dịch vụ | Cổng cư dân có mục Tình trạng dịch vụ: cắt nước, cắt điện, thang máy đang diễn ra, sắp diễn ra trong 7 ngày, vừa khôi phục trong 24 giờ. Cư dân nhập mã căn là biết căn mình có bị ảnh hưởng không. Số liệu lấy từ sổ Gián đoạn dịch vụ trong SSR Điều Hành mỗi lần Ban Quản lý đồng bộ. |
| Khảo sát hài lòng | Mục Tình hình vận hành có phiếu góp ý hằng tháng: cấp nước, vệ sinh, an ninh, phản hồi của Ban Quản lý, mỗi mục 1 đến 5 sao. Mỗi căn góp ý một lần mỗi tháng. SSR Điều Hành tự lấy kết quả vào trang Giám sát dịch vụ. |
