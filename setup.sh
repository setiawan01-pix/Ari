#!/bin/bash

echo "🤖 Setup Bot Telegram Python"
echo "=============================="

# Cek apakah Python terinstall
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak ditemukan. Silakan install Python3 terlebih dahulu."
    exit 1
fi

echo "✅ Python3 ditemukan: $(python3 --version)"

# Cek apakah pip terinstall
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 tidak ditemukan. Silakan install pip3 terlebih dahulu."
    exit 1
fi

echo "✅ pip3 ditemukan"

# Install dependensi
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies berhasil diinstall"
else
    echo "❌ Gagal menginstall dependencies"
    exit 1
fi

# Cek token bot
if [ -z "$BOT_TOKEN" ]; then
    echo ""
    echo "⚠️  Token bot belum diset!"
    echo ""
    echo "🔧 Cara mengatur token bot:"
    echo "1. Buka Telegram dan cari @BotFather"
    echo "2. Kirim /newbot untuk membuat bot baru"
    echo "3. Salin token yang diberikan"
    echo "4. Set environment variable:"
    echo "   export BOT_TOKEN='your_token_here'"
    echo ""
    echo "Atau edit file telegram_bot.py langsung"
    echo ""
else
    echo "✅ Token bot sudah diset"
fi

echo ""
echo "🚀 Bot siap dijalankan!"
echo "Jalankan dengan perintah: python3 telegram_bot.py"
echo ""