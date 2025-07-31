from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    """Main menu with access options"""
    keyboard = [
        [InlineKeyboardButton("🧪 Trial 1 Jam", callback_data='trial')],
        [InlineKeyboardButton("🔐 Premium (Berbayar)", callback_data='premium')],
        [InlineKeyboardButton("ℹ️ Info Bot", callback_data='info')]
    ]
    return InlineKeyboardMarkup(keyboard)

def features_menu():
    """Features menu for active users"""
    keyboard = [
        [InlineKeyboardButton("📁 Fitur Konversi", callback_data='conversion_features')],
        [InlineKeyboardButton("🛠️ File Tools", callback_data='file_tools')],
        [InlineKeyboardButton("🧾 Input Manual", callback_data='manual_input')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def conversion_menu():
    """Conversion features menu"""
    keyboard = [
        [InlineKeyboardButton("📂 TXT ➝ VCF (Format TUTOR KIKS)", callback_data='conv_txt_to_vcf')],
        [InlineKeyboardButton("✂️ TXT ➝ TXT (Split)", callback_data='conv_split_txt')],
        [InlineKeyboardButton("📤 VCF ➝ TXT", callback_data='conv_vcf_to_txt')],
        [InlineKeyboardButton("📊 XLS ➝ VCF", callback_data='conv_xls_to_vcf')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_features')]
    ]
    return InlineKeyboardMarkup(keyboard)

def file_tools_menu():
    """File tools menu"""
    keyboard = [
        [InlineKeyboardButton("📎 Gabungkan File", callback_data='merge_files')],
        [InlineKeyboardButton("🔍 Cek Duplikat", callback_data='check_duplicates')],
        [InlineKeyboardButton("➕ Tambah Kontak", callback_data='add_contact')],
        [InlineKeyboardButton("✏️ Rename File", callback_data='rename_file')],
        [InlineKeyboardButton("❌ Hapus Nomor", callback_data='delete_number')],
        [InlineKeyboardButton("✂️ Pecah File", callback_data='split_file_tool')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_features')]
    ]
    return InlineKeyboardMarkup(keyboard)

def premium_menu():
    """Premium subscription menu"""
    keyboard = [
        [InlineKeyboardButton("1 Hari - Rp 5.000", callback_data='premium_1_hari')],
        [InlineKeyboardButton("7 Hari - Rp 25.000", callback_data='premium_7_hari')],
        [InlineKeyboardButton("30 Hari - Rp 75.000", callback_data='premium_30_hari')],
        [InlineKeyboardButton("Lifetime - Rp 200.000", callback_data='premium_lifetime')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def admin_menu():
    """Admin panel menu"""
    keyboard = [
        [InlineKeyboardButton("📢 Broadcast", callback_data='admin_broadcast')],
        [InlineKeyboardButton("💳 Ganti QR / Metode Bayar", callback_data='admin_payment')],
        [InlineKeyboardButton("🛠️ Atur Harga Premium", callback_data='admin_prices')],
        [InlineKeyboardButton("📆 Jadwal Konversi", callback_data='admin_schedule')],
        [InlineKeyboardButton("👥 Lihat Daftar User", callback_data='admin_users')],
        [InlineKeyboardButton("➕ Tambah User Manual", callback_data='admin_adduser')],
        [InlineKeyboardButton("❌ Kick User", callback_data='admin_kick')],
        [InlineKeyboardButton("🖊️ Ubah Teks Sambutan", callback_data='admin_welcome')],
        [InlineKeyboardButton("📋 Log Aktivitas", callback_data='admin_logs')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def cancel_button():
    """Cancel button for conversations"""
    keyboard = [[InlineKeyboardButton("❌ Batal", callback_data='cancel')]]
    return InlineKeyboardMarkup(keyboard)

def back_button(callback_data: str):
    """Back button with custom callback"""
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data=callback_data)]]
    return InlineKeyboardMarkup(keyboard)

def file_type_menu():
    """File type selection for manual input"""
    keyboard = [
        [InlineKeyboardButton("📄 Simpan sebagai TXT", callback_data='save_as_txt')],
        [InlineKeyboardButton("📇 Simpan sebagai VCF", callback_data='save_as_vcf')],
        [InlineKeyboardButton("❌ Batal", callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(keyboard)

def duplicate_action_menu():
    """Menu for duplicate handling"""
    keyboard = [
        [InlineKeyboardButton("🔘 Hapus duplikat & kirim ulang", callback_data='remove_duplicates')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_file_tools')]
    ]
    return InlineKeyboardMarkup(keyboard)
