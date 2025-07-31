#!/bin/bash

echo "🤖 Bot Konversi Kontak Telegram"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak ditemukan!"
    echo "   Silakan install Python3 terlebih dahulu"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 tidak ditemukan!"
    echo "   Silakan install pip3 terlebih dahulu"
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Gagal install dependencies!"
        exit 1
    fi
    echo "✅ Dependencies berhasil diinstall"
fi

# Create necessary folders
echo "📁 Creating folders..."
mkdir -p temp qr_codes
echo "✅ Folders berhasil dibuat"

# Check if main_simple.py exists
if [ ! -f "main_simple.py" ]; then
    echo "❌ File main_simple.py tidak ditemukan!"
    echo "   Pastikan file tersebut ada di folder yang sama"
    exit 1
fi

echo ""
echo "🚀 Starting bot..."
echo "📱 Token: 8198867479:AAEtUhyTID-crNvg8fohpfvTYkYtIEDz6aQ"
echo "👑 Admin ID: 8141075788"
echo "================================"

# Run the bot
python3 main_simple.py