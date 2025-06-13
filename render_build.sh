#!/usr/bin/env bash
# exit on error
set -o errexit

# Cập nhật pip
pip install --upgrade pip

# Cài đặt các gói Python
pip install -r requirements.txt

# Tạo thư mục migrations nếu chưa tồn tại
mkdir -p migrations/versions

# Khởi tạo cơ sở dữ liệu nếu cần
export FLASK_APP=wsgi:app

# Kiểm tra xem đã có migrations chưa
if [ ! -f "migrations/README" ]; then
    flask db init
fi

# Tạo và áp dụng migrations
flask db migrate -m "Initial migration"
flask db upgrade
