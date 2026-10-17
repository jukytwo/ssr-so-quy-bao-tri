# Bật phần hỏi AI (Gemini miễn phí) cho nút Hỏi đáp

Nút **Hỏi đáp** có ở cả hai mục Quỹ bảo trì và Điều hành. Câu hỏi nào có câu trả lời sẵn trên trang thì trả lời ngay, không cần AI. Câu nào trang chưa có thì hỏi Gemini, kèm các đoạn liên quan nhất của trang để câu trả lời bám sát báo cáo.

Chưa làm các bước dưới đây thì nút Hỏi đáp vẫn chạy, chỉ là không có phần AI. Làm một lần, khoảng 10 phút.

## Bước 1. Lấy khóa Gemini miễn phí

1. Mở https://aistudio.google.com/apikey, đăng nhập tài khoản Google của anh.
2. Bấm **Create API key**, chép khóa (chuỗi bắt đầu bằng `AIza`).
3. Không gắn thẻ thanh toán. Không gắn thẻ thì chỉ dùng hạn mức miễn phí, không bao giờ bị tính tiền.

## Bước 2. Tạo máy chủ hỏi đáp trên Google Apps Script

1. Mở https://script.google.com, bấm **Dự án mới**, đặt tên `SSR Hoi dap`.
2. Xóa mã mẫu, dán toàn bộ nội dung file `may-chu/HoiDap.gs`, bấm lưu.
3. Bấm **Cài đặt dự án** (bánh răng bên trái), kéo xuống **Thuộc tính tập lệnh**, thêm:

| Thuộc tính | Giá trị |
|---|---|
| `GEMINI_API_KEY` | khóa vừa chép ở Bước 1 |
| `DAILY_LIMIT` | tùy chọn, số câu hỏi AI tối đa mỗi ngày, mặc định 300 |

4. Quay lại trình soạn mã, chọn hàm `kiemTraHoiDap`, bấm **Chạy**, cho phép quyền khi Google hỏi. Nhật ký thực thi phải có hai dòng **ĐẠT**.

## Bước 3. Triển khai thành web app

1. Bấm **Triển khai**, **Tùy chọn triển khai mới**, chọn **Ứng dụng web**.
2. **Thực thi với tư cách**: Tôi. **Người có quyền truy cập**: Bất kỳ ai.
3. Bấm **Triển khai**, chép địa chỉ dạng `https://script.google.com/macros/s/.../exec`.

## Bước 4. Nối trang với máy chủ

Mở file `web/hoi-dap/config.js` trên GitHub (bấm biểu tượng bút chì), dán địa chỉ ở Bước 3 vào giữa hai dấu nháy:

```
window.SSR_HOIDAP = { url: "https://script.google.com/macros/s/.../exec" };
```

Bấm **Commit changes**. Khoảng 1 phút sau, nút Hỏi đáp trên trang có thêm phần AI. Anh cũng có thể gửi địa chỉ cho Claude để dán và đẩy lên giúp.

## Thêm văn bản để hỏi đáp trả lời sát hơn

Quy chế hoạt động của Ban Quản trị, Nội quy nhà chung cư, Quy chế thu chi... hiện chưa có toàn văn trên trang, nên các câu hỏi về điều khoản riêng của SSR AI chỉ trả lời được theo quy định chung. Muốn thêm:

1. Chép toàn văn sang một tệp chữ `.txt`, dòng đầu là tên văn bản, mỗi điều bắt đầu bằng "Điều 1.", "Điều 2."...
2. Đặt vào thư mục `web/hoi-dap/tai-lieu/`.
3. Dựng lại kho nội dung: `node src/hoidap/build_kb.js` (hoặc nhờ Claude làm), rồi đẩy lên.

## Lưu ý

- Khóa Gemini chỉ nằm ở Thuộc tính tập lệnh, không nằm trong trang công khai.
- Ở gói miễn phí, Google có thể dùng nội dung câu hỏi để cải thiện sản phẩm. Khung hỏi đáp đã nhắc cư dân không ghi tên, số điện thoại, số căn hộ.
- Hết lượt trong ngày, trang báo cư dân hỏi lại hôm sau; câu trả lời có sẵn trên trang vẫn dùng bình thường.
- Câu trả lời AI có thể sai, trang luôn ghi rõ là tham khảo, không thay cho tư vấn pháp lý. Chỉ dẫn cho AI trong `HoiDap.gs` theo Bộ nguyên tắc xác minh thông tin (bản 17/10/2026): chỉ trả lời từ tài liệu của trang, riêng quy định pháp luật nhà chung cư được dùng văn bản chính thức còn hiệu lực và ghi rõ là ngoài tài liệu; nguồn web chỉ hiện nguồn chính thức và báo chí lớn.
- Cập nhật mã máy chủ: **Triển khai**, **Quản lý các bản triển khai**, bút chì, chọn phiên bản mới. Địa chỉ giữ nguyên.
