@echo off
chcp 65001 >nul

echo 🤖 Bot Konversi Kontak Telegram
echo ================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python tidak ditemukan!
    echo    Silakan install Python terlebih dahulu
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip tidak ditemukan!
    echo    Silakan install pip terlebih dahulu
    pause
    exit /b 1
)

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Gagal install dependencies!
        pause
        exit /b 1
    )
    echo ✅ Dependencies berhasil diinstall
)

REM Create necessary folders
echo 📁 Creating folders...
if not exist "temp" mkdir temp
if not exist "qr_codes" mkdir qr_codes
echo ✅ Folders berhasil dibuat

REM Check if main_simple.py exists
if not exist "main_simple.py" (
    echo ❌ File main_simple.py tidak ditemukan!
    echo    Pastikan file tersebut ada di folder yang sama
    pause
    exit /b 1
)

echo.
echo 🚀 Starting bot...
echo 📱 Token: 8198867479:AAEtUhyTID-crNvg8fohpfvTYkYtIEDz6aQ
echo 👑 Admin ID: 8141075788
echo ================================

REM Run the bot
python main_simple.py

pause