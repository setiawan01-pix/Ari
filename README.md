# 🤖 Bot Telegram Python

Bot Telegram sederhana yang dibuat dengan Python menggunakan library `python-telegram-bot`.

## 📋 Fitur

- ✅ Command dasar (`/start`, `/help`, `/info`, `/ping`)
- ✅ Respon pesan teks otomatis
- ✅ Error handling
- ✅ Logging untuk debugging
- ✅ Emoji dan formatting yang menarik

## 🚀 Cara Menjalankan

### 1. Install Dependensi

```bash
pip install -r requirements.txt
```

### 2. Dapatkan Token Bot

1. Buka Telegram dan cari **@BotFather**
2. Kirim pesan `/newbot`
3. Ikuti instruksi untuk membuat bot baru
4. Salin token yang diberikan

### 3. Set Token Bot

**Cara 1: Environment Variable (Direkomendasikan)**
```bash
export BOT_TOKEN="your_bot_token_here"
```

**Cara 2: Edit File Langsung**
Edit file `telegram_bot.py` dan ganti `YOUR_BOT_TOKEN_HERE` dengan token bot Anda.

### 4. Jalankan Bot

```bash
python telegram_bot.py
```

## 📱 Perintah yang Tersedia

| Perintah | Deskripsi |
|----------|-----------|
| `/start` | Pesan selamat datang |
| `/help` | Menampilkan bantuan |
| `/info` | Informasi tentang bot |
| `/ping` | Test koneksi bot |

## 💬 Respon Pesan

Bot akan merespon pesan teks dengan cara berikut:
- **Sapaan** (`halo`, `hello`, `hi`, `hai`) → Respon ramah
- **Ucapan terima kasih** → Respon sopan
- **Pertanyaan** (mengandung `?`) → Saran menggunakan `/help`
- **Pesan lain** → Echo pesan dengan saran perintah

## 🔧 Struktur Kode

```
telegram_bot.py
├── Command Handlers
│   ├── start_command() - Pesan selamat datang
│   ├── help_command() - Bantuan
│   ├── info_command() - Informasi bot
│   └── ping_command() - Test koneksi
├── Message Handler
│   └── echo_message() - Respon pesan teks
├── Error Handler
│   └── error_handler() - Penanganan error
└── Main Function
    └── main() - Inisialisasi dan menjalankan bot
```

## 🛠️ Customisasi

### Menambah Command Baru

```python
async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk command baru"""
    await update.message.reply_text("Pesan dari command baru!")

# Tambahkan di fungsi main()
application.add_handler(CommandHandler("new", new_command))
```

### Menambah Respon Pesan

Edit fungsi `echo_message()` untuk menambah logika respon sesuai kebutuhan.

## 📝 Logging

Bot menggunakan logging untuk debugging. Log akan menampilkan:
- Waktu eksekusi
- Level log (INFO, ERROR, dll)
- Pesan detail

## 🚨 Troubleshooting

### Error: Token bot belum diset
- Pastikan token bot sudah diset dengan benar
- Cek environment variable atau edit file langsung

### Error: Module not found
- Install dependensi: `pip install -r requirements.txt`

### Bot tidak merespon
- Pastikan bot sudah dijalankan
- Cek log untuk error
- Pastikan token bot valid

## 📚 Referensi

- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## 🤝 Kontribusi

Silakan berkontribusi dengan:
- Melaporkan bug
- Menambah fitur baru
- Memperbaiki dokumentasi

## 📄 Lisensi

Proyek ini menggunakan lisensi MIT.
