@echo off
setlocal enabledelayedexpansion

:: Màu sắc
set ESC=
set RESET=%ESC%[0m
set BOLD=%ESC%[1m
set RED=%ESC%[91m
set GREEN=%ESC%[92m
set YELLOW=%ESC%[93m
set BLUE=%ESC%[94m
set CYAN=%ESC%[96m

:: Hiển thị tiêu đề
echo %CYAN%%BOLD%
 _   _           _       _          _   _             
| | | |_ __   __| | __ _| |_ ___   | | | |_ __   __ _ 
| | | | '_ \ / _` |/ _` | __/ _ \  | | | | '_ \ / _` |
| |_| | |_) | (_| | (_| | ||  __/  | |_| | |_) | (_| |
 \___/| .__/ \__,_|\__,_|\__\___|   \___/| .__/ \__,_|
      |_|                                 |_|          %RESET%

echo %GREEN%[INFO]%RESET% Bắt đầu cập nhật dự án...

:: Kiểm tra xem đã kích hoạt môi trường ảo chưa
if "%VIRTUAL_ENV%"=="" (
    if exist "venv\Scripts\activate" (
        echo %YELLOW%[WARN]%RESET% Đang kích hoạt môi trường ảo...
        call venv\Scripts\activate
        if %ERRORLEVEL% neq 0 (
            echo %RED%[ERROR]%RESET% Không thể kích hoạt môi trường ảo
            pause
            exit /b 1
        )
    else
        echo %RED%[ERROR]%RESET% Không tìm thấy môi trường ảo. Vui lòng chạy setup.bat trước
        pause
        exit /b 1
    )
)

:: Cập nhật pip
echo %GREEN%[INFO]%RESET% Đang cập nhật pip...
python -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
    echo %RED%[ERROR]%RESET% Không thể cập nhật pip
    pause
    exit /b 1
)

:: Cập nhật các gói cần thiết
echo %GREEN%[INFO]%RESET% Đang cập nhật các thư viện...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo %RED%[ERROR]%RESET% Có lỗi khi cập nhật các thư viện
    pause
    exit /b 1
)

:: Cập nhật các gói phát triển (nếu có)
if exist "requirements-dev.txt" (
    echo %GREEN%[INFO]%RESET% Đang cập nhật các thư viện phát triển...
    pip install -r requirements-dev.txt
    if %ERRORLEVEL% neq 0 (
        echo %YELLOW%[WARN]%RESET% Có lỗi khi cập nhật các thư viện phát triển
    )
)

:: Cập nhật cơ sở dữ liệu
echo %GREEN%[INFO]%RESET% Đang kiểm tra cập nhật cơ sở dữ liệu...
set FLASK_APP=wsgi:app
flask db upgrade
if %ERRORLEVEL% neq 0 (
    echo %YELLOW%[WARN]%RESET% Có lỗi khi cập nhật cơ sở dữ liệu
)

:: Kiểm tra các file cấu hình
echo %GREEN%[INFO]%RESET% Kiểm tra các file cấu hình...
if not exist ".env" (
    if exist ".env.example" (
        echo %YELLOW%[WARN]%RESET% File .env không tồn tại, đang tạo từ .env.example...
        copy ".env.example" ".env" >nul
        if %ERRORLEVEL% equ 0 (
            echo %YELLOW%[WARN]%RESET% Đã tạo file .env từ .env.example
            echo %YELLOW%[WARN]%RESET% Vui lý cập nhật file .env với cấu hình phù hợp
        ) else (
            echo %RED%[ERROR]%RESET% Không thể tạo file .env
        )
    ) else (
        echo %RED%[ERROR]%RESET% Không tìm thấy file .env và .env.example
    )
)

:: Tạo các thư mục cần thiết
mkdir logs 2>nul
mkdir app\static\uploads 2>nul
mkdir app\static\outputs 2>nul
mkdir app\static\temp 2>nul

echo %GREEN%[INFO]%RESET% Cập nhật hoàn tất!
echo %GREEN%[INFO]%RESET% Bạn có thể chạy ứng dụng bằng lệnh: %BLUE%start.bat%RESET%

pause
