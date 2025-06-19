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
  ____ _                            
 / ___| | ___  __ _ _ __   ___ _ __ 
| |   | |/ _ \/ _` | '_ \ / _ \ '__|
| |___| |  __/ (_| | | | |  __/ |   
 \____|_|\___|\__,_|_| |_|\___|_|   
                                    %RESET%

echo %GREEN%[INFO]%RESET% Bắt đầu dọn dẹp dự án...

:: Xóa các thư mục cache Python
echo %YELLOW%[CLEAN]%RESET% Đang xóa các thư mục cache Python...
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        echo Xóa thư mục: %%~dpd%%~nxd
        rmdir /s /q "%%d" 2>nul
    )
)

:: Xóa các file .pyc, .pyo, .pyd
for /r . %%f in (*.pyc, *.pyo, *.pyd) do (
    if exist "%%f" (
        echo Xóa file: %%~nxf
        del /q "%%f" 2>nul
    )
)

:: Xóa thư mục build và dist
for %%d in (build, dist, *.egg-info) do (
    if exist "%%~d" (
        echo Xóa thư mục: %%~d
        rmdir /s /q "%%~d" 2>nul
    )
)

:: Xóa file .coverage và thư mục htmlcov
if exist ".coverage" (
    echo Xóa file: .coverage
    del /q ".coverage" 2>nul
)

if exist "htmlcov" (
    echo Xóa thư mục: htmlcov
    rmdir /s /q "htmlcov" 2>nul
)

:: Xóa các file log
if exist "logs" (
    echo Xóa các file log...
    del /q "logs\*" 2>nul
)

:: Xóa các file tạm
for %%d in (app\static\temp, app\static\uploads, app\static\outputs) do (
    if exist "%%~d" (
        echo Xóa nội dung thư mục: %%~d
        del /q "%%~d\*" 2>nul
    )
)

echo %GREEN%[INFO]%RESET% Đã hoàn thành dọn dẹp!
pause
