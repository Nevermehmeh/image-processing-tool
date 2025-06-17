@echo off
echo Đang thiết lập môi trường...

REM Tạo môi trường ảo mới
echo Tạo môi trường ảo...
python -m venv venv
call .\venv\Scripts\activate

REM Cập nhật pip
echo Cập nhật pip...
python -m pip install --upgrade pip

REM Cài đặt các gói cần thiết
echo Cài đặt các thư viện...
pip install numpy==1.26.4
pip install -r requirements.txt

REM Tạo file .env
echo Tạo file cấu hình...
if not exist .env (
    copy .env.example .env
    echo Đã tạo file .env từ .env.example
) else (
    echo File .env đã tồn tại, bỏ qua...
)

REM Khởi tạo cơ sở dữ liệu
echo Khởi tạo cơ sở dữ liệu...
set FLASK_APP=wsgi:app
flask db upgrade

echo.
echo =======================================
echo Thiết lập hoàn tất!
echo Để chạy ứng dụng, gõ lệnh sau:
echo .\venv\Scripts\activate
python run.py
echo =======================================

pause
