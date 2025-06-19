@echo off
setlocal enabledelayedexpansion

echo **********************************************
echo *        THIET LAP MOI TRUONG PHAT TRIEN       *
echo **********************************************

REM Kiểm tra Python version
echo Kiem tra phien ban Python...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Loi: Python khong duoc cai dat hoac khong co trong PATH
    echo Vui long cai dat Python 3.8+ va thu lai
    pause
    exit /b 1
)

REM Lấy phiên bản Python
for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo Tim thay Python phiên bản: %PYTHON_VERSION%

REM Kiểm tra phiên bản Python
for /f "tokens=1,2,3 delims=." %%a in ("%PYTHON_VERSION%") do (
    if %%a lss 3 (
        echo Loi: Yeu cau Python 3.8+ nhung tim thay %%a.%%b.%%c
        pause
        exit /b 1
    )
    if %%b lss 8 (
        echo Canh bao: Khuyen dung Python 3.8+ nhung tim thay %%a.%%b.%%c
        echo Co the xay ra loi khong tuong thich
        timeout /t 3 >nul
    )
)

REM Tạo môi trường ảo mới
echo.
echo TAO MOI TRUONG AO...
if not exist "venv\" (
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Loi: Khong the tao moi truong ao
        pause
        exit /b 1
    )
    echo Da tao moi truong ao thanh cong
) else (
    echo Moi truong ao da ton tai, bo qua...
)

call venv\Scripts\activate
if %ERRORLEVEL% neq 0 (
    echo Loi: Khong the kich hoat moi truong ao
    pause
    exit /b 1
)

REM Cập nhật pip
echo.
echo CAP NHAT PIP...
python -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
    echo Loi: Khong the cap nhat pip
    pause
    exit /b 1
)

REM Cài đặt các gói cần thiết
echo.
echo CAI DAT THU VIEN...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Loi: Khong the cai dat cac thu vien
    pause
    exit /b 1
)

REM Cài đặt các gói phát triển (tùy chọn)
echo.
echo CAI DAT THU VIEN PHAT TRIEN (tuy chon)...
if exist "requirements-dev.txt" (
    pip install -r requirements-dev.txt
) else (
    echo Khong tim thay requirements-dev.txt, bo qua...
)

REM Tạo file .env
echo.
echo TAO FILE CAU HINH...
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo Da tao file .env tu .env.example
    ) else (
        echo Khong tim thay file .env.example, tao file .env trong
        echo. > .env
    )
    
    echo Vui long chinh sua file .env voi cac thong tin phu hop
    timeout /t 3 >nul
) else (
    echo File .env da ton tai, bo qua...
)

REM Khởi tạo cơ sở dữ liệu
echo.
echo KHOI TAO CO SO DU LIEU...
set FLASK_APP=wsgi:app
set FLASK_ENV=development
flask db upgrade
if %ERRORLEVEL% neq 0 (
    echo Canh bao: Co loi khi khoi tao co so du lieu
    echo Co the do chua cau hinh DATABASE_URL trong file .env
    timeout /t 3 >nul
)

REM Tạo các thư mục cần thiết
mkdir logs 2>nul
mkdir app\static\uploads 2>nul
mkdir app\static\outputs 2>nul
mkdir app\static\temp 2>nul

echo.
echo ===================================================
echo  THIET LAP HOAN TAT!
echo ===================================================
echo.
echo De chay ung dung, su dung mot trong cac lenh sau:
echo.
echo 1. Che do phat trien (truc tiep):
echo      python run.py
echo.
echo 2. Su dung Gunicorn (cho moi truong production):
echo      gunicorn --worker-class=gevent --worker-connections=1000 --workers=4 --timeout 120 --bind :5000 wsgi:app
echo.
echo 3. Su dung Docker Compose (can cai dat Docker):
echo      docker-compose up -d
echo.
echo 4. Chay voi Docker:
echo      docker build -t image-processor .
echo      docker run -d -p 5000:5000 --env-file .env image-processor
echo.
echo ===================================================
echo.

pause
