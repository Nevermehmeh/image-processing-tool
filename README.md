# Image Region Extractor

Ứng dụng web cho phép tạo template và trích xuất các vùng ảnh từ ảnh gốc dựa trên template đã định nghĩa.

## Tính năng chính

- **Tạo template**: Định nghĩa các vùng ảnh con trên ảnh gốc
- **Trích xuất ảnh**: Sử dụng template để tự động cắt các vùng ảnh từ ảnh mới
- **Giao diện trực quan**: Kéo thả để định vị và điều chỉnh kích thước vùng ảnh
- **Hỗ trợ ảnh lớn**: Xử lý ảnh lên đến 6000x6000px

## Triển khai lên Render

1. **Fork repository** này về tài khoản GitHub của bạn
2. Đăng nhập vào [Render](https://render.com)
3. Tạo mới Web Service và kết nối với repository của bạn
4. Cấu hình như sau:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
5. Thêm các biến môi trường cần thiết (xem file `.env.example`)
6. Tạo PostgreSQL database và kết nối với Web Service
7. Nhấn Deploy

## Biến môi trường

Tạo file `.env` từ `.env.example` và điền các giá trị phù hợp:

```
FLASK_APP=wsgi:app
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
UPLOAD_FOLDER=static/uploads
```

## Phát triển cục bộ

1. Tạo và kích hoạt môi trường ảo:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Trên Windows
   source venv/bin/activate  # Trên macOS/Linux
   ```

2. Cài đặt dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Chạy ứng dụng:
   ```bash
   flask run
   ```

4. Truy cập http://localhost:5000

## Yêu cầu hệ thống

- Python 3.8+
- pip (trình quản lý gói Python)

## Cài đặt

1. **Sao chép repository**
   ```bash
   git clone [repository-url]
   cd image-region-extractor
   ```

2. **Tạo và kích hoạt môi trường ảo (khuyến nghị)**
   ```bash
   # Trên Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Trên macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Cài đặt các thư viện phụ thuộc**
   ```bash
   pip install -r requirements.txt
   ```

## Sử dụng

1. **Khởi động ứng dụng**
   ```bash
   python run.py
   ```

2. **Truy cập ứng dụng**
   Mở trình duyệt và truy cập: [http://localhost:5000](http://localhost:5000)

## Hướng dẫn sử dụng

### Tạo template mới

1. Nhấn vào "Create Template" trong thanh điều hướng
2. Nhập tên cho template
3. Tải lên ảnh gốc
4. Điều chỉnh kích thước và vị trí của các vùng ảnh bằng cách kéo thả
5. Nhấn "Save Template" để lưu

### Trích xuất vùng ảnh

1. Nhấn vào "Extract Regions" trong thanh điều hướng
2. Chọn template từ danh sách
3. Tải lên ảnh cần xử lý
4. Ứng dụng sẽ tự động cắt các vùng ảnh theo template
5. Tải về các vùng ảnh đã được cắt

## Cấu trúc thư mục

```
image-region-extractor/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/
│   ├── templates/
│   ├── __init__.py
│   ├── models/
│   └── routes/
├── config.py
├── requirements.txt
└── run.py
```

## Giấy phép

Dự án này được phân phối theo giấy phép MIT. Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## Đóng góp

Đóng góp luôn được chào đón! Vui lòng đọc [hướng dẫn đóng góp](CONTRIBUTING.md) để biết thêm chi tiết.

## Tác giả

[Your Name] - [Your Email]

---

*Dự án được phát triển như một công cụ mã nguồn mở.*
