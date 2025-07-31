#!/usr/bin/env python3
"""
Bot Konversi Kontak Telegram
File utama untuk menjalankan bot
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'telegram',
        'pandas',
        'openpyxl',
        'xlrd'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Dependensi yang diperlukan belum terinstall:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install dependensi dengan perintah:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def create_folders():
    """Create necessary folders"""
    folders = ['temp', 'qr_codes']
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✅ Folder '{folder}' berhasil dibuat")

def main():
    """Main function"""
    print("🤖 Bot Konversi Kontak Telegram")
    print("=" * 40)
    
    # Check dependencies
    print("🔍 Mengecek dependensi...")
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ Semua dependensi terinstall")
    
    # Create folders
    print("📁 Membuat folder yang diperlukan...")
    create_folders()
    
    # Check if main_simple.py exists
    if not os.path.exists('main_simple.py'):
        print("❌ File main_simple.py tidak ditemukan!")
        print("   Pastikan file tersebut ada di folder yang sama")
        sys.exit(1)
    
    print("\n🚀 Menjalankan bot...")
    print("📱 Token: 8198867479:AAEtUhyTID-crNvg8fohpfvTYkYtIEDz6aQ")
    print("👑 Admin ID: 8141075788")
    print("=" * 40)
    
    try:
        # Import and run the bot
        from main_simple import main as run_bot
        run_bot()
    except KeyboardInterrupt:
        print("\n⏹️ Bot dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Pastikan token bot valid dan koneksi internet stabil")

if __name__ == '__main__':
    main()