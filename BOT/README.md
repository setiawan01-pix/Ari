# Bot Konversi Kontak Telegram

Bot Telegram untuk konversi dan manipulasi file kontak dengan sistem akses trial dan premium.

## Fitur Utama

### 🔐 Sistem Akses
- **Trial**: 1 jam gratis
- **Premium**: Berbayar dengan berbagai paket (1 hari, 7 hari, 30 hari, lifetime)

### 📁 Fitur Konversi
1. **TXT ➝ VCF** (Format TUTOR KIKS)
   - Konversi file TXT berisi nomor telepon ke format VCF
   - Dapat mengatur nama file, nama kontak, jumlah per file, dan urutan awal

2. **TXT ➝ TXT (Split)**
   - Membagi file TXT besar menjadi beberapa file kecil
   - Dapat mengatur jumlah baris per file

3. **VCF ➝ TXT**
   - Ekstrak nomor telepon dari file VCF ke TXT
   - Satu nomor per baris

4. **XLS ➝ VCF**
   - Konversi file Excel ke format VCF
   - Kolom A = Nama, Kolom B = Nomor

### 🛠️ File Tools
1. **Gabungkan File**
   - Menggabungkan beberapa file TXT/VCF menjadi satu

2. **Cek Duplikat**
   - Mengecek dan menghapus nomor duplikat

3. **Tambah Kontak**
   - Menambahkan kontak baru ke file

4. **Rename File**
   - Mengubah nama file

5. **Hapus Nomor**
   - Menghapus nomor tertentu dari file

6. **Pecah File**
   - Memecah file besar menjadi beberapa bagian

7. **Input Manual**
   - Input kontak secara manual dan simpan ke file

### 👑 Fitur Admin
1. **Broadcast**
   - Kirim pesan ke semua user aktif

2. **Kelola User**
   - Lihat daftar user
   - Tambah user manual
   - Kick user

3. **Pengaturan**
   - Ganti QR code/metode pembayaran
   - Atur harga premium
   - Ubah teks sambutan

4. **Log Aktivitas**
   - Lihat log aktivitas user

## Instalasi

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Buat folder yang diperlukan**
```bash
mkdir temp qr_codes
```

3. **Jalankan bot**
```bash
python main_simple.py
```

## Konfigurasi

Bot sudah dikonfigurasi dengan:
- **Token Bot**: 8198867479:AAEtUhyTID-crNvg8fohpfvTYkYtIEDz6aQ
- **Admin ID**: 8141075788

## Penggunaan

### Untuk User
1. Start bot dengan `/start`
2. Pilih Trial atau Premium
3. Pilih fitur yang diinginkan
4. Ikuti instruksi bot

### Untuk Admin
1. Gunakan command admin:
   - `/adduser <id> <hari>` - Tambah user manual
   - `/kick <id>` - Hapus user
   - `/ubahsambutan <pesan>` - Ubah pesan sambutan

2. Akses menu admin melalui tombol di bot

## Dependensi

- `python-telegram-bot==20.7` - Library Telegram Bot
- `pandas==2.1.4` - Untuk membaca file Excel
- `openpyxl==3.1.2` - Untuk file Excel .xlsx
- `xlrd==2.0.1` - Untuk file Excel .xls

## Catatan

- Bot menggunakan sistem trial 1 jam per user
- File temporary akan otomatis dihapus setelah diproses
- Log aktivitas disimpan di `log.txt`
- Data user disimpan di `user_data.json`
- Pastikan folder `temp` dan `qr_codes` memiliki permission write

## Support

Untuk bantuan dan support, hubungi admin bot.