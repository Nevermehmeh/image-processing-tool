@echo off
setlocal enabledelayedexpansion

:: Tên ứng dụng
set APP_NAME=Image Processor

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
  ___                 _         ____            _            _             
 |_ _|_ __ ___  __ _| |_ ___  |  _ \ _ __ ___ | |_ ___  ___| |_ ___  _ __ 
  | || '_ ` _ \/ _` | __/ _ \ | |_) | '__/ _ \| __/ _ \/ __| __/ _ \| '__|
  | || | | | | | (_| | ||  __/ |  __/| | | (_) | ||  __/ (__| || (_) | |   
 |___|_| |_| |_|\__,_|\__\___| |_|   |_|  \___/ \__\___|\___|\__\___/|_|   
%RESET%

:: Kiểm tra xem đã kích hoạt môi trường ảo chưa
if not "%VIRTUAL_ENV%"=="" (
    echo %GREEN%[INFO]%RESET% Môi trường ảo đã được kích hoạt: %VIRTUAL_ENV%
) else (
    if exist "venv\Scripts\activate" (
        echo %YELLOW%[WARN]%RESET% Đang kích hoạt môi trường ảo...
        call venv\Scripts\activate
        if %ERRORLEVEL% neq 0 (
            echo %RED%[ERROR]%RESET% Không thể kích hoạt môi trường ảo
            pause
            exit /b 1
        )
    ) else (
        echo %RED%[ERROR]%RESET% Không tìm thấy môi trường ảo. Vui lòng chạy setup.bat trước
        pause
        exit /b 1
    )
)

:: Kiểm tra file .env
if not exist ".env" (
    if exist ".env.example" (
        echo %YELLOW%[WARN]%RESET% File .env không tồn tại, đang tạo từ .env.example...
        copy ".env.example" ".env" >nul
        if %ERRORLEVEL% neq 0 (
            echo %RED%[ERROR]%RESET% Không thể tạo file .env
            pause
            exit /b 1
        )
        echo %YELLOW%[WARN]%RESET% Vui lý cập nhật file .env với cấu hình phù hợp
        timeout /t 3 >nul
    ) else (
        echo %RED%[ERROR]%RESET% Không tìm thấy file .env và .env.example
        pause
        exit /b 1
    )
)

:: Tạo các thư mục cần thiết
mkdir logs 2>nul
mkdir app\static\uploads 2>nul
mkdir app\static\outputs 2>nul
mkdir app\static\temp 2>nul

:: Lấy thông tin cấu hình từ file .env
set FLASK_APP=wsgi:app
set FLASK_ENV=development

:: In thông tin cấu hình
echo %GREEN%[INFO]%RESET% Đang khởi động %APP_NAME%...
echo %CYAN%[CONFIG]%RESET% FLASK_APP = %FLASK_APP%
echo %CYAN%[CONFIG]%RESET% FLASK_ENV = %FLASK_ENV%

:: Kiểm tra xem có cần cập nhật cơ sở dữ liệu không
flask db current 2>&1 | findstr "No such command" >nul
if %ERRORLEVEL% equ 0 (
    echo %YELLOW%[WARN]%RESET% Không tìm thấy lệnh 'flask db'. Đảm bảo đã cài đặt Flask-Migrate
) else (
    echo %GREEN%[INFO]%RESET% Kiểm tra cập nhật cơ sở dữ liệu...
    flask db upgrade
    if %ERRORLEVEL% neq 0 (
        echo %YELLOW%[WARN]%RESET% Có lỗi khi cập nhật cơ sở dữ liệu. Tiếp tục khởi động...
    )
)

:: Chạy ứng dụng
echo %GREEN%[INFO]%RESET% Đang khởi động máy chủ phát triển...
echo %GREEN%[INFO]%RESET% Nhấn Ctrl+C để dừng ứng dụng

echo %CYAN%[URL]%RESET% Ứng dụng có sẵn tại: %BLUE%http://localhost:5000/%RESET%

:: Chạy ứng dụng
python run.py %*

:: Xử lý khi dừng ứng dụng
:cleanup
if %ERRORLEVEL% neq 0 (
    echo %RED%[ERROR]%RESET% Ứng dụng đã dừng với mã lỗi %ERRORLEVEL%
) else (
    echo %GREEN%[INFO]%RESET% Ứng dụng đã dừng
)

pause
