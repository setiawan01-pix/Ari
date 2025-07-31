# Telegram Bot

Bot Telegram yang dapat mengkonversi file kontak dan melakukan berbagai operasi file.

## Instalasi

1. Clone repository ini
2. Install dependencies:
   ```bash
   cd BOT
   pip install -r requirements.txt
   ```

3. Konfigurasi environment variables:
   ```bash
   cp .env.example .env
   # Edit .env dengan token bot dan admin ID Anda
   ```

4. Jalankan bot:
   ```bash
   python3 main.py
   ```

## Konfigurasi

Buat file `.env` di direktori BOT dengan konfigurasi berikut:

```
BOT_TOKEN=token_bot_telegram_anda
ADMIN_ID=id_admin_anda
```

## Fitur

- Konversi file TXT ke VCF
- Merge file kontak
- Hapus duplikat kontak
- Split file besar
- Broadcast pesan
- Manajemen user premium
- Scheduler untuk tugas otomatis

## Keamanan

- Token bot dan data sensitif menggunakan environment variables
- File konfigurasi tidak disimpan di git
- Cache Python diabaikan dari version control
