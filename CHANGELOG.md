# Lịch sử Thay đổi

Tất cả các thay đổi đáng chú ý đối với dự án Image Processor sẽ được ghi lại trong tài liệu này.

Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
và dự án tuân thủ [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Thêm mới
- Hỗ trợ xử lý ảnh lớn lên đến 9000x9000 pixel
- Tích hợp thư viện pyvips để tối ưu hiệu suất xử lý ảnh
- Thêm API endpoint mới cho việc trích xuất vùng ảnh
- Hỗ trợ xử lý bất đồng bộ cho các tác vụ nặng
- Thêm hệ thống quản lý tệp tạm thời tự động dọn dẹp

### Thay đổi
- Tái cấu trúc mã nguồn để dễ bảo trì hơn
- Cải thiện xử lý lỗi và thông báo cho người dùng
- Tối ưu hóa sử dụng bộ nhớ khi xử lý ảnh lớn
- Cập nhật các phụ thuộc lên phiên bản mới nhất

### Sửa lỗi
- Sửa lỗi tràn bộ nhớ khi xử lý ảnh có kích thước lớn
- Sửa lỗi hiển thị thanh tiến trình trên một số trình duyệt
- Sửa lỗi định dạng đầu ra ảnh không chính xác
- Sửa lỗi bảo mật liên quan đến tải lên tệp

## [0.1.0] - 2025-06-19
### Thêm mới
- Phát hành phiên bản đầu tiên của Image Processor
- Hỗ trợ các thao tác xử lý ảnh cơ bản
- Giao diện người dùng đơn giản và trực quan
- Hỗ trợ đa nền tảng

---

## Hướng dẫn Cập nhật

### Định dạng Phiên bản

Mỗi phiên bản phải tuân theo định dạng `MAJOR.MINOR.PATCH`:

1. **MAJOR**: Khi có thay đổi không tương thích ngược
2. **MINOR**: Khi thêm chức năng mới nhưng vẫn tương thích ngược
3. **PATCH**: Khi sửa lỗi và cải tiến nhỏ

### Cách Thêm Mục Nhập Mới

1. **Chọn loại thay đổi**: Thêm vào một trong các mục `Thêm mới`, `Thay đổi`, hoặc `Sửa lỗi`
2. **Mô tả ngắn gọn**: Sử dụng thì quá khứ và bắt đầu bằng chữ in hoa
3. **Tham chiếu issue**: Thêm số tham chiếu issue trong ngoặc đơn (nếu có)

Ví dụ:
```
### Sửa lỗi
- Sửa lỗi hiển thị thanh tiến trình (#123)
```

## Ghi chú Phát hành

### 0.1.0
- Phát hành đầu tiên của ứng dụng Image Processor
- Bao gồm các tính năng cơ bản để xử lý ảnh

---

Tài liệu này được tạo ra dựa trên [Keep a Changelog](https://keepachangelog.com/).
