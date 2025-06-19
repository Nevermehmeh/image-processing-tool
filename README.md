# 🖼️ Image Region Extractor

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0.x-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Ứng dụng web cho phép tạo template và trích xuất các vùng ảnh từ ảnh gốc dựa trên template đã định nghĩa, hỗ trợ xử lý ảnh lớn lên đến 9000x9000px.

## 🌟 Tính năng nổi bật

- **🎨 Tạo template trực quan**: Định nghĩa các vùng ảnh con dễ dàng bằng giao diện kéo thả
- **⚡ Xử lý ảnh mạnh mẽ**: Hỗ trợ ảnh lớn lên đến 9000x9000px
- **🚀 Hiệu năng cao**: Sử dụng pyvips để xử lý ảnh hiệu quả, tiết kiệm bộ nhớ
- **🔒 Bảo mật**: Kiểm tra đầu vào chặt chẽ, giới hạn kích thước file
- **📊 Logging chi tiết**: Dễ dàng debug và giám sát hệ thống
- **🐳 Hỗ trợ Docker**: Triển khai đơn giản với Docker
- **🌐 Triển khai đa nền tảng**: Hỗ trợ Render, Heroku, VPS

## 🚀 Bắt đầu nhanh

### Yêu cầu hệ thống

- Python 3.8+
- Redis (tùy chọn, cho xử lý bất đồng bộ)
- pip
- libvips (để cài đặt pyvips)

### Cài đặt môi trường phát triển

1. **Clone repository**
   ```bash
   git clone https://github.com/your-username/image-region-extractor.git
   cd image-region-extractor
   ```

2. **Tạo và kích hoạt môi trường ảo**
   ```bash
   # Trên Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Trên macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Cài đặt dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Dành cho phát triển
   ```

4. **Cấu hình biến môi trường**
   Tạo file `.env` từ `.env.example` và cập nhật các giá trị phù hợp:
   ```bash
   cp .env.example .env
   ```

5. **Khởi động ứng dụng**
   ```bash
   python run.py
   ```

6. **Truy cập ứng dụng**
   Mở trình duyệt và truy cập: http://localhost:5000

## 🐳 Triển khai với Docker

### Sử dụng Docker Compose (Khuyến nghị)

```bash
# Khởi động tất cả dịch vụ
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng và xóa container
docker-compose down
```

### Build và chạy thủ công

```bash
# Build image
docker build -t image-region-extractor .

# Chạy container
docker run -d --name image_processor \
  -p 5000:5000 \
  -v $(pwd)/uploads:/app/app/static/uploads \
  -v $(pwd)/outputs:/app/app/static/outputs \
  -v $(pwd)/temp:/app/app/static/temp \
  --env-file .env \
  image-region-extractor
```

## ☁️ Triển khai lên Render

1. **Fork repository** này về tài khoản GitHub của bạn
2. Đăng nhập vào [Render](https://render.com)
3. Tạo mới Web Service và kết nối với repository của bạn
4. Cấu hình như sau:
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     flask db upgrade
     ```
   - **Start Command**: 
     ```bash
     gunicorn --worker-class=gevent --worker-connections=1000 --workers=4 --timeout 120 --bind :$PORT wsgi:app
     ```
5. Thêm các biến môi trường cần thiết từ file `.env.example`
6. Tạo PostgreSQL database và kết nối với Web Service
7. Nhấn Deploy

## 🛠 Công nghệ sử dụng

- **Backend**: Python, Flask, SQLAlchemy, Redis, Celery
- **Xử lý ảnh**: pyvips, Pillow
- **Frontend**: HTML5, CSS3, JavaScript, jQuery, Bootstrap 5
- **Cơ sở dữ liệu**: PostgreSQL, SQLite (phát triển)
- **Triển khai**: Docker, Gunicorn, Nginx
- **CI/CD**: GitHub Actions
- **Giám sát**: Sentry, Prometheus

## 📄 Cấu trúc dự án

```
image-region-extractor/
├── app/                    # Mã nguồn chính
│   ├── static/             # Tài nguyên tĩnh (CSS, JS, hình ảnh)
│   │   ├── uploads/        # Thư mục lưu ảnh tải lên
│   │   ├── outputs/        # Thư mục lưu ảnh đã xử lý
│   │   └── temp/           # Thư mục tạm
│   ├── templates/          # Template HTML
│   ├── __init__.py         # Khởi tạo ứng dụng
│   ├── models.py           # Định nghĩa models
│   ├── routes.py           # Định tuyến URL
│   └── utils/              # Tiện ích hỗ trợ
│       ├── image_utils.py   # Xử lý ảnh
│       └── validators.py    # Kiểm tra dữ liệu
├── migrations/             # Migrations database
├── tests/                  # Kiểm thử
├── .env.example            # Mẫu biến môi trường
├── .gitignore              # Git ignore
├── .dockerignore           # Docker ignore
├── .pre-commit-config.yaml # Cấu hình pre-commit
├── docker-compose.yml      # Docker Compose
├── Dockerfile              # Dockerfile
├── requirements.txt        # Thư viện chính
├── requirements-dev.txt    # Thư viện phát triển
└── README.md               # Tài liệu dự án
```

## 🤝 Đóng góp

Đóng góp luôn được chào đón! Hãy xem [hướng dẫn đóng góp](CONTRIBUTING.md) để biết thêm chi tiết.

1. Fork repository
2. Tạo nhánh mới (`git checkout -b feature/AmazingFeature`)
3. Commit các thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên nhánh (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📄 Giấy phép

Dự án này được phân phối theo giấy phép **MIT**. Xem file `LICENSE` để biết thêm chi tiết.

## 🙏 Cảm ơn

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [pyvips](https://github.com/libvips/pyvips) - Xử lý ảnh hiệu năng cao
- [Bootstrap](https://getbootstrap.com/) - Giao diện người dùng
- [Render](https://render.com) - Nền tảng triển khai

---

<div align="center">
  <sub>Được tạo bởi</sub> 💖
  <br>
  <br>
  <a href="https://github.com/your-username">
    <img src="https://avatars.githubusercontent.com/your-username" width="100" alt="Your Name">
  </a>
  <br>
  <sub><b>Your Name</b></sub>
  <br>
  <sub>
    <a href="https://your-website.com">🌐 Website</a> | 
    <a href="https://twitter.com/your-handle">🐦 Twitter</a> | 
    <a href="https://linkedin.com/in/your-profile">💼 LinkedIn</a>
  </sub>
</div>
