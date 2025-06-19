#!/bin/bash

# Màu sắc
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Hàm in thông báo lỗi
function error_exit {
    echo -e "${RED}[ERROR] $1${NC}" >&2
    exit 1
}

# Hàm in thông báo thành công
function success_msg {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

# Hàm in thông báo thông tin
function info_msg {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Hàm in cảnh báo
function warning_msg {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Kiểm tra xem script có được chạy với quyền root không
if [ "$EUID" -ne 0 ]; then 
    warning_msg "Vui lòng chạy script với quyền root (sudo)."
    exit 1
fi

# Cập nhật hệ thống
info_msg "Đang cập nhật hệ thống..."
apt-get update && apt-get upgrade -y || error_exit "Không thể cập nhật hệ thống."

# Cài đặt các gói cần thiết
info_msg "Đang cài đặt các gói cần thiết..."
apt-get install -y python3 python3-pip python3-venv nginx supervisor || error_exit "Không thể cài đặt các gói cần thiết."

# Tạo thư mục cho ứng dụng
APP_DIR="/opt/image_processor"
info_msg "Đang tạo thư mục ứng dụng tại $APP_DIR..."
mkdir -p $APP_DIR

# Sao chép mã nguồn
info_msg "Đang sao chép mã nguồn..."
cp -r . $APP_DIR/ || error_exit "Không thể sao chép mã nguồn."
cd $APP_DIR || error_exit "Không thể chuyển vào thư mục ứng dụng."

# Tạo và kích hoạt môi trường ảo
info_msg "Đang tạo môi trường ảo..."
python3 -m venv venv || error_exit "Không thể tạo môi trường ảo."
source venv/bin/activate || error_exit "Không thể kích hoạt môi trường ảo."

# Cài đặt các phụ thuộc
info_msg "Đang cài đặt các thư viện Python..."
pip install --upgrade pip || error_exit "Không thể cập nhật pip."
pip install -r requirements.txt || error_exit "Không thể cài đặt các thư viện."

# Tạo file .env nếu chưa tồn tại
if [ ! -f ".env" ]; then
    warning_msg "File .env không tồn tại, đang tạo từ .env.example..."
    cp .env.example .env || error_exit "Không thể tạo file .env."
    warning_msg "Vui lý cập nhật file .env với cấu hình phù hợp trước khi tiếp tục."
    exit 1
fi

# Tạo các thư mục cần thiết
info_msg "Đang tạo các thư mục cần thiết..."
mkdir -p logs app/static/uploads app/static/outputs app/static/temp
chmod -R 755 logs app/static

# Cấu hình Gunicorn
info_msg "Đang cấu hình Gunicorn..."
cat > /etc/systemd/system/image_processor.service <<EOL
[Unit]
Description=Image Processor
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --worker-class=gevent --worker-connections=1000 --workers=4 --timeout 120 --bind unix:image_processor.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
EOL

# Cấu hình Nginx
info_msg "Đang cấu hình Nginx..."
cat > /etc/nginx/sites-available/image_processor <<EOL
server {
    listen 80;
    server_name your_domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/image_processor.sock;
    }

    location /static/ {
        alias $APP_DIR/app/static/;
    }
}
EOL

# Kích hoạt cấu hình Nginx
ln -s /etc/nginx/sites-available/image_processor /etc/nginx/sites-enabled || error_exit "Không thể kích hoạt cấu hình Nginx."
nginx -t || error_exit "Cấu hình Nginx không hợp lệ."

# Khởi động lại các dịch vụ
info_msg "Đang khởi động lại các dịch vụ..."
systemctl daemon-reload
systemctl start image_processor
systemctl enable image_processor
systemctl restart nginx

# Mở cổng tường lửa
info_msg "Đang mở cổng tường lửa..."
ufw allow 'Nginx Full'

success_msg "Triển khai thành công!"
echo -e "${CYN}Ứng dụng đã được triển khai tại: http://your_domain.com${NC}"
echo -e "${YELLOW}Vui lý cập nhật file cấu hình Nginx với tên miền thực tế của bạn.${NC}"
