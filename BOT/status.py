#!/usr/bin/env python3
"""
Status Bot - Menampilkan informasi status bot
"""

import os
import json
from datetime import datetime

def check_bot_status():
    """Check bot status and show information"""
    print("🤖 STATUS BOT KONVERSI KONTAK TELEGRAM")
    print("=" * 50)
    
    # Check configuration
    print("📋 KONFIGURASI:")
    print(f"   Token Bot: 8198867479:AAEtUhyTID-crNvg8fohpfvTYkYtIEDz6aQ")
    print(f"   Admin ID: 8141075788")
    print()
    
    # Check files
    print("📁 FILE STATUS:")
    files_to_check = [
        ("main_simple.py", "File utama bot"),
        ("config.py", "File konfigurasi"),
        ("requirements.txt", "File dependensi"),
        ("user_data.json", "Data user"),
        ("customization.json", "Data kustomisasi"),
        ("log.txt", "Log aktivitas")
    ]
    
    for filename, description in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"   ✅ {filename} ({description}) - {size} bytes")
        else:
            print(f"   ❌ {filename} ({description}) - Tidak ditemukan")
    
    print()
    
    # Check folders
    print("📂 FOLDER STATUS:")
    folders_to_check = [
        ("temp", "Folder temporary file"),
        ("qr_codes", "Folder QR code"),
        ("handlers", "Folder handlers"),
        ("utils", "Folder utilities"),
        ("file_tools", "Folder file tools"),
        ("admin_access", "Folder admin features")
    ]
    
    for foldername, description in folders_to_check:
        if os.path.exists(foldername):
            file_count = len([f for f in os.listdir(foldername) if os.path.isfile(os.path.join(foldername, f))])
            print(f"   ✅ {foldername}/ ({description}) - {file_count} files")
        else:
            print(f"   ❌ {foldername}/ ({description}) - Tidak ditemukan")
    
    print()
    
    # Check user data
    print("👥 USER STATISTICS:")
    if os.path.exists("user_data.json"):
        try:
            with open("user_data.json", "r", encoding="utf-8") as f:
                user_data = json.load(f)
            
            total_users = len(user_data)
            trial_users = sum(1 for user in user_data.values() if user.get("status") == "trial")
            premium_users = sum(1 for user in user_data.values() if user.get("status") == "premium")
            expired_users = sum(1 for user in user_data.values() if user.get("status") == "expired")
            
            print(f"   Total Users: {total_users}")
            print(f"   Trial Users: {trial_users}")
            print(f"   Premium Users: {premium_users}")
            print(f"   Expired Users: {expired_users}")
        except Exception as e:
            print(f"   ❌ Error membaca user data: {e}")
    else:
        print("   Belum ada user terdaftar")
    
    print()
    
    # Check log
    print("📋 LOG STATUS:")
    if os.path.exists("log.txt"):
        try:
            with open("log.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            total_logs = len(lines)
            if total_logs > 0:
                last_log = lines[-1].strip()
                print(f"   Total Logs: {total_logs}")
                print(f"   Last Log: {last_log}")
            else:
                print("   Belum ada log aktivitas")
        except Exception as e:
            print(f"   ❌ Error membaca log: {e}")
    else:
        print("   File log tidak ditemukan")
    
    print()
    
    # Check dependencies
    print("📦 DEPENDENCIES:")
    dependencies = [
        ("telegram", "python-telegram-bot"),
        ("pandas", "pandas"),
        ("openpyxl", "openpyxl"),
        ("xlrd", "xlrd")
    ]
    
    for module, package in dependencies:
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Belum terinstall")
    
    print()
    print("=" * 50)
    print("✅ Status check selesai!")

if __name__ == "__main__":
    check_bot_status()