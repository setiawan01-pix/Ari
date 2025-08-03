# 📚 Dokumentasi Lengkap Bot Telegram Premium

## 🎯 Ringkasan Fitur

Bot Telegram ini dilengkapi dengan sistem admin, manajemen langganan, dan tools konversi yang lengkap. Berikut adalah dokumentasi detail untuk semua fitur yang tersedia.

---

## 👑 FITUR ADMIN (OWNER BOT)

### 🔐 Akses Admin
- **Admin ID:** Ditetapkan di `config.py` pada variabel `admin_ids`
- **Contoh:** `admin_ids = [123456789, 987654321]`
- **Keamanan:** Hanya user dengan ID yang terdaftar yang dapat mengakses fitur admin

### 🔁 Perpanjang Langganan User

#### Fungsi
Admin dapat memperpanjang masa aktif user secara manual dengan berbagai durasi.

#### Logika Proses
1. **Admin ketik `/admin`** atau tekan tombol 🔁 Perpanjang
2. **Bot minta ID user** (atau reply ke user)
3. **Bot minta durasi tambahan** (1 hari, 7 hari, 30 hari, dst.)
4. **Sistem update expired_date** user di database
5. **Bot konfirmasi:** ✅ Langganan diperpanjang

#### Command Admin
```bash
/admin
```

#### Durasi yang Tersedia
- 1 Hari
- 7 Hari  
- 30 Hari
- 90 Hari
- 365 Hari

#### Log Aktivitas
- Semua aktivitas admin dicatat di database
- Log mencakup: admin ID, aksi, target user, deskripsi, timestamp

### 📊 Status Langganan

#### Fitur
- **Statistik lengkap** semua user
- **User yang akan habis** dalam 7 hari ke depan
- **User yang sudah habis**
- **Total user aktif vs expired**

#### Informasi yang Ditampilkan
```
📊 STATUS LANGGANAN

👥 Total User: 150
✅ Langganan Aktif: 120
❌ Langganan Habis: 30

⚠️ Akan Habis (7 hari ke depan):
• John Doe (ID: 123456) - 3 hari lagi
• Jane Smith (ID: 789012) - 5 hari lagi

❌ Sudah Habis:
• Bob Wilson (ID: 345678) - 2 hari yang lalu
```

### 👥 Daftar User

#### Fitur
- **Daftar 20 user terbaru**
- **Status langganan** setiap user
- **Tanggal expired** yang detail
- **Indikator visual** (✅ untuk aktif, 🆓 untuk gratis)

#### Format Tampilan
```
👥 DAFTAR USER (20 terbaru)

1. ✅ John Doe (ID: 123456789)
   📅 Status: premium
   ⏰ Expired: 15/12/2024

2. 🆓 Jane Smith (ID: 987654321)
   📅 Status: free
```

### 📋 Log Admin

#### Fitur
- **Riwayat aktivitas admin** (10 terbaru)
- **Detail aksi** yang dilakukan
- **Timestamp** setiap aktivitas
- **Target user** yang terpengaruh

#### Format Log
```
📋 LOG AKTIVITAS ADMIN (10 terbaru)

🕐 15/12/2024 14:30
👤 Admin ID: 123456789
📝 Aksi: extend_subscription
🎯 Target: 987654321
📄 Deskripsi: Perpanjang langganan 30 hari
```

### 🔔 Test Notifikasi

#### Fungsi
- **Test sistem notifikasi** ke admin
- **Verifikasi** bot dapat mengirim pesan
- **Debugging** sistem notifikasi

---

## 🔔 NOTIFIKASI OTOMATIS

### ⏰ Sistem Notifikasi

#### Fungsi
Memberi tahu user jika langganannya akan habis atau sudah habis secara otomatis.

#### Logika Sistem
1. **Bot cek database setiap jam** (cron time)
2. **Jika sisa waktu = 1 hari** → Kirim: "⏳ Langganan Anda tersisa 1 hari"
3. **Jika expired** → Kirim: "❌ Langganan Anda sudah habis"
4. **Batasi akses menu** sampai diperpanjang

### 📅 Jadwal Notifikasi

#### Notifikasi 7 Hari Sebelum Habis
```
⚠️ PERINGATAN LANGGANAN

Halo John! 👋

📅 Langganan Anda akan habis dalam 7 hari.
📅 Tanggal expired: 22/12/2024

🔁 Untuk memperpanjang langganan, silakan hubungi admin.
💬 Gunakan command /contact untuk menghubungi admin.

Terima kasih telah menggunakan layanan kami! 🙏
```

#### Notifikasi 1 Hari Sebelum Habis
```
⏳ PERINGATAN LANGGANAN

Halo John! 👋

⚠️ Langganan Anda akan HABIS BESOK!
📅 Tanggal expired: 15/12/2024

🔁 Untuk memperpanjang langganan, silakan hubungi admin.
💬 Gunakan command /contact untuk menghubungi admin.

Terima kasih telah menggunakan layanan kami! 🙏
```

#### Notifikasi Sudah Habis
```
❌ LANGGANAN HABIS

Halo John! 👋

❌ Langganan Anda SUDAH HABIS!
📅 Tanggal expired: 14/12/2024
⏰ Habis 1 hari yang lalu

🔒 Akses fitur premium telah dibatasi.
🔁 Untuk mengaktifkan kembali, silakan perpanjang langganan.
💬 Hubungi admin dengan command /contact

Terima kasih telah menggunakan layanan kami! 🙏
```

### 🔄 Sistem Anti-Spam
- **Notifikasi hanya dikirim sekali per hari** per user
- **Log notifikasi** disimpan di database
- **Rate limiting** untuk menghindari spam

---

## 🛠️ FITUR KONVERSI & TOOLS

### 🔄 Konversi

#### Base64
```bash
# Encode
base64 Hello World
# Output: SGVsbG8gV29ybGQ=

# Decode  
decode SGVsbG8gV29ybGQ=
# Output: Hello World
```

#### Hash Functions
```bash
# MD5
md5 Hello World
# Output: b10a8db164e0754105b7a99be72e3fe5

# SHA256
sha256 Hello World
# Output: a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e
```

#### Unit Conversion
```bash
# Temperature
celsius_to_fahrenheit(25) → 77.0°F
fahrenheit_to_celsius(77) → 25.0°C

# Distance
km_to_miles(10) → 6.21 miles
miles_to_km(6.21) → 10.0 km

# Weight
kg_to_lbs(50) → 110.23 lbs
lbs_to_kg(110.23) → 50.0 kg
```

### 📝 Text Tools

#### Hitung Karakter
```
📊 ANALISIS TEKS

📝 Teks: "Hello World 123!"
📊 Total Karakter: 16
📝 Total Kata: 3
📄 Total Baris: 1
🚫 Spasi: 2
🔤 Huruf: 10
🔢 Angka: 3
🔧 Karakter Khusus: 1
```

#### Manipulasi Teks
```bash
# Uppercase
"hello world" → "HELLO WORLD"

# Lowercase  
"HELLO WORLD" → "hello world"

# Title Case
"hello world" → "Hello World"

# Reverse
"hello" → "olleh"

# Remove Spaces
"hello world" → "helloworld"
```

### 🕐 DateTime Tools

#### Waktu Saat Ini
```
🕐 WAKTU SAAT INI

📅 Tanggal: 15/12/2024
⏰ Waktu: 14:30:25
📊 Timestamp: 1702642225
🌐 ISO: 2024-12-15T14:30:25.123456
📝 Format: Sunday, 15 December 2024 14:30:25
```

#### Konversi Timestamp
```bash
# Timestamp to DateTime
1702642225 → 2024-12-15 14:30:25

# DateTime to Timestamp
2024-12-15 14:30:25 → 1702642225
```

### 📊 JSON Tools

#### Format JSON
```json
// Input
{"name":"John","age":30,"city":"New York"}

// Output (Formatted)
{
  "name": "John",
  "age": 30,
  "city": "New York"
}
```

#### Minify JSON
```json
// Input (Formatted)
{
  "name": "John",
  "age": 30,
  "city": "New York"
}

// Output (Minified)
{"name":"John","age":30,"city":"New York"}
```

#### Validasi JSON
```bash
# Valid JSON
{
  "valid": true,
  "type": "dict",
  "size": 45
}

# Invalid JSON
{
  "valid": false,
  "error": "Expecting ',' delimiter",
  "line": 2,
  "column": 5
}
```

### 🧮 Kalkulator

#### Operasi yang Didukung
- **Penjumlahan:** `+`
- **Pengurangan:** `-`
- **Perkalian:** `*`
- **Pembagian:** `/`
- **Pangkat:** `**`
- **Kurung:** `()` untuk prioritas

#### Contoh Penggunaan
```bash
calc 2 + 2
# Output: 4

calc 10 * 5
# Output: 50

calc (2 + 3) * 4
# Output: 20

calc 100 / 4
# Output: 25
```

### 🔗 URL Tools

#### Ekstrak URL
```bash
# Input: "Visit https://example.com and https://google.com"
# Output: ["https://example.com", "https://google.com"]
```

#### Validasi URL
```bash
# Valid
https://example.com → true
http://google.com → true

# Invalid
not-a-url → false
ftp://example.com → false
```

---

## 📊 SISTEM DATABASE

### 🗄️ Struktur Database

#### Tabel Users
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    subscription_status TEXT DEFAULT 'free',
    expired_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabel Subscriptions
```sql
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    subscription_type TEXT,
    duration_days INTEGER,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    status TEXT DEFAULT 'active',
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
```

#### Tabel Admin Actions
```sql
CREATE TABLE admin_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER,
    action_type TEXT,
    target_user_id INTEGER,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabel Notifications
```sql
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    notification_type TEXT,
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
```

### 🔍 Query Utama

#### Cek Status Langganan
```python
def get_subscription_status(user_id: int) -> Dict[str, Any]:
    # Mengembalikan status lengkap user
    # - active: langganan aktif
    # - expired: langganan habis
    # - free: akun gratis
```

#### User yang Akan Habis
```python
def get_expiring_subscriptions(days_threshold: int = 1) -> List[Dict[str, Any]]:
    # Mengembalikan user yang langganannya akan habis dalam X hari
```

#### User yang Sudah Habis
```python
def get_expired_subscriptions() -> List[Dict[str, Any]]:
    # Mengembalikan user yang langganannya sudah habis
```

---

## 🚀 COMMAND REFERENCE

### 👤 User Commands

| Command | Deskripsi | Akses |
|---------|-----------|-------|
| `/start` | Pesan selamat datang | Semua |
| `/help` | Bantuan lengkap | Semua |
| `/status` | Cek status langganan | Semua |
| `/contact` | Hubungi admin | Semua |
| `/tools` | Menu tools | Semua |
| `/info` | Informasi bot | Semua |
| `/ping` | Test koneksi | Semua |

### 👑 Admin Commands

| Command | Deskripsi | Akses |
|---------|-----------|-------|
| `/admin` | Panel admin | Admin only |

### 🛠️ Quick Tools

| Command | Deskripsi | Contoh |
|---------|-----------|--------|
| `calc` | Kalkulator | `calc 2 + 2` |
| `base64` | Encode Base64 | `base64 Hello` |
| `decode` | Decode Base64 | `decode SGVsbG8=` |
| `md5` | Generate MD5 | `md5 Hello` |
| `sha256` | Generate SHA256 | `sha256 Hello` |

---

## 🔧 KONFIGURASI

### ⚙️ File Config

#### config.py
```python
class BotConfig:
    # Token bot
    token: str = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    
    # Admin IDs
    admin_ids: list = [123456789]  # Ganti dengan ID admin Anda
    
    # Pengaturan notifikasi
    enable_notifications: bool = True
    
    # Pengaturan database
    db_path: str = "bot_database.db"
```

### 🔐 Environment Variables

#### BOT_TOKEN
```bash
export BOT_TOKEN="your_bot_token_here"
```

### 📁 Struktur File
```
bot_telegram/
├── telegram_bot.py          # Main bot file
├── config.py               # Konfigurasi
├── database.py             # Database manager
├── admin_handlers.py       # Admin functions
├── notification_system.py  # Notification system
├── tools.py               # Conversion tools
├── requirements.txt        # Dependencies
├── setup.sh               # Setup script
├── run_bot.sh             # Run script
├── README.md              # Basic documentation
└── DOCUMENTATION.md       # This file
```

---

## 🚨 TROUBLESHOOTING

### ❌ Error Umum

#### Token Bot Belum Diset
```
❌ Error: Token bot belum diset!
🔧 Cara mengatur token:
1. Set environment variable: export BOT_TOKEN='your_token_here'
2. Atau edit file config.py
```

#### Database Error
```
❌ Error: Database tidak dapat diakses
🔧 Solusi:
1. Cek permission file database
2. Restart bot
3. Cek disk space
```

#### Notifikasi Tidak Terkirim
```
❌ Error: Notifikasi gagal dikirim
🔧 Solusi:
1. Cek koneksi internet
2. Cek token bot valid
3. Cek user tidak memblokir bot
```

### 🔍 Debug Mode

#### Enable Logging
```python
# Di config.py
log_level: str = "DEBUG"
```

#### Log File
```bash
# Log akan disimpan di console
# Format: timestamp - module - level - message
```

---

## 📈 MONITORING & MAINTENANCE

### 📊 Metrics yang Dimonitor

#### User Statistics
- Total user terdaftar
- User aktif vs expired
- User baru per hari
- User yang akan habis

#### System Performance
- Response time bot
- Database query performance
- Notification delivery rate
- Error rate

### 🔄 Maintenance Tasks

#### Daily
- Backup database
- Check notification logs
- Monitor error logs

#### Weekly
- Clean old notification logs
- Optimize database
- Update admin statistics

#### Monthly
- Full system backup
- Performance review
- Feature updates

---

## 🔐 SECURITY

### 🛡️ Keamanan Admin
- **ID Validation:** Hanya ID yang terdaftar yang dapat akses admin
- **Action Logging:** Semua aktivitas admin dicatat
- **Rate Limiting:** Mencegah spam admin commands

### 🔒 Data Protection
- **User Data:** Hanya admin yang dapat akses data user
- **Token Security:** Token bot disimpan dengan aman
- **Database:** SQLite dengan proper indexing

### 🚫 Anti-Spam
- **Message Rate Limiting:** Mencegah spam pesan
- **Notification Cooldown:** Notifikasi maksimal 1x per hari
- **Command Validation:** Validasi input user

---

## 📞 SUPPORT

### 🆘 Cara Mendapatkan Bantuan

#### Untuk User
1. Gunakan command `/help` untuk bantuan
2. Gunakan command `/contact` untuk hubungi admin
3. Cek status langganan dengan `/status`

#### Untuk Admin
1. Gunakan command `/admin` untuk panel admin
2. Cek log aktivitas di menu admin
3. Test notifikasi dengan fitur test

### 📧 Contact Information
- **Admin:** @admin_username
- **Email:** admin@example.com
- **Telegram:** https://t.me/admin_username

---

## 📄 LISENSI

Proyek ini menggunakan lisensi MIT. Silakan lihat file LICENSE untuk detail lebih lanjut.

---

## 🤝 KONTRIBUSI

Kontribusi sangat diterima! Silakan:
1. Fork repository
2. Buat feature branch
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

---

**© 2024 Bot Telegram Premium. Dibuat dengan ❤️ menggunakan Python dan python-telegram-bot.**