#!/bin/bash

echo "🤖 Menjalankan Bot Telegram..."
echo "=============================="

# Cek apakah file bot ada
if [ ! -f "telegram_bot.py" ]; then
    echo "❌ File telegram_bot.py tidak ditemukan!"
    echo "Pastikan Anda berada di direktori yang benar."
    exit 1
fi

# Cek apakah Python terinstall
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak ditemukan!"
    exit 1
fi

# Cek apakah dependensi terinstall
if ! python3 -c "import telegram" 2>/dev/null; then
    echo "⚠️  Dependensi belum terinstall. Menjalankan setup..."
    if [ -f "setup.sh" ]; then
        chmod +x setup.sh
        ./setup.sh
    else
        echo "❌ File setup.sh tidak ditemukan!"
        echo "Install manual: pip3 install -r requirements.txt"
        exit 1
    fi
fi

# Cek token bot
if [ -z "$BOT_TOKEN" ]; then
    echo "⚠️  Token bot belum diset sebagai environment variable"
    echo "Bot akan menggunakan token dari file (jika ada)"
fi

echo "✅ Semua cek berhasil"
echo "🚀 Menjalankan bot..."
echo ""
echo "📱 Bot akan mulai merespon pesan"
echo "🛑 Tekan Ctrl+C untuk menghentikan"
echo ""

# Jalankan bot
python3 telegram_bot.py