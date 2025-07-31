from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📁 Fitur Konversi", callback_data='conversion_features')],
        [InlineKeyboardButton("🛠️ File Tools", callback_data='file_tools')],
        [InlineKeyboardButton("🧪 Trial 1 Jam", callback_data='trial')],
        [InlineKeyboardButton("🔐 Premium (Berbayar)", callback_data='premium')],
        [InlineKeyboardButton("ℹ️ Info Bot", callback_data='info')]
    ]
    return InlineKeyboardMarkup(keyboard)

def txt_menu():
    keyboard = [
        [InlineKeyboardButton("Konversi ke VCF", callback_data='txt_to_vcf')],
        [InlineKeyboardButton("Split TXT", callback_data='split_txt')]
    ]
    return InlineKeyboardMarkup(keyboard)

def conversion_menu():
    keyboard = [
        [InlineKeyboardButton("TXT ➝ VCF", callback_data='conv_txt_to_vcf')],
        [InlineKeyboardButton("TXT ➝ TXT (Split)", callback_data='conv_split_txt')],
        [InlineKeyboardButton("VCF ➝ TXT", callback_data='conv_vcf_to_txt')],
        [InlineKeyboardButton("XLS ➝ VCF", callback_data='conv_xls_to_vcf')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

def file_tools_menu():
    keyboard = [
        [InlineKeyboardButton("Gabungkan File", callback_data='merge_files')],
        [InlineKeyboardButton("Cek Duplikat", callback_data='check_duplicates')],
        [InlineKeyboardButton("Tambah Kontak", callback_data='add_contact')],
        [InlineKeyboardButton("Rename File", callback_data='rename_file')],
        [InlineKeyboardButton("Hapus Nomor", callback_data='delete_number')],
        [InlineKeyboardButton("Pecah File", callback_data='split_file_tool')],
        [InlineKeyboardButton("Input Manual", callback_data='manual_input')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main')],
    ]
    return InlineKeyboardMarkup(keyboard)
