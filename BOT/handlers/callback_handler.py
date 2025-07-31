from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime, timedelta
from utils.caching import get_user_data, update_user_data, get_customization_data, get_prices_data

from handlers.file_handler import ASK_FILENAME, ASK_CONTACTS_PER_FILE as ASK_LINES_PER_FILE
from .menus import file_tools_menu, conversion_menu, main_menu

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    user_data = get_user_data()

    if query.data == 'trial':
        user_data[user_id] = {
            "status": "trial",
            "start_time": str(datetime.now()),
            "expire_time": str(datetime.now() + timedelta(hours=1))
        }
        update_user_data(user_data)
        await query.edit_message_text(text="Anda telah memulai masa percobaan 1 jam.")

    elif query.data == 'premium':
        # Logic for premium subscription will be added here
        await query.edit_message_text(text="Fitur premium akan segera hadir.")

    elif query.data == 'info':
        await query.edit_message_text(text="Bot ini memiliki banyak fitur untuk membantu Anda mengelola kontak.")

    elif query.data == 'txt_to_vcf':
        await query.edit_message_text("Masukkan nama file dasar:")
        return ASK_FILENAME

    elif query.data == 'split_txt':
        await query.edit_message_text("Berapa jumlah baris per file?")
        return ASK_LINES_PER_FILE

    elif query.data == 'file_tools':
        await query.edit_message_text("Pilih alat yang ingin Anda gunakan:", reply_markup=file_tools_menu())

    elif query.data == 'conversion_features':
        await query.edit_message_text("Pilih jenis konversi:", reply_markup=conversion_menu())
    
    # File Tools Handlers
    elif query.data == 'merge_files':
        await query.edit_message_text("📁 Fitur Gabungkan File\n\nKirim file-file yang ingin Anda gabungkan (satu per satu), lalu ketik /done")
        
    elif query.data == 'check_duplicates':
        await query.edit_message_text("🔍 Fitur Cek Duplikat\n\nKirim file untuk mengecek duplikat kontak dengan caption /checkduplicates")
        
    elif query.data == 'add_contact':
        await query.edit_message_text("➕ Fitur Tambah Kontak\n\nKirim file, lalu berikan nama dan nomor kontak yang ingin ditambahkan")
        
    elif query.data == 'rename_file':
        await query.edit_message_text("🏷️ Fitur Rename File\n\nKirim file yang ingin direname")
        
    elif query.data == 'delete_number':
        await query.edit_message_text("🗑️ Fitur Hapus Nomor\n\nKirim file, lalu berikan nomor yang ingin dihapus")
        
    elif query.data == 'split_file_tool':
        await query.edit_message_text("✂️ Fitur Pecah File\n\nKirim file yang ingin dipecah")
        
    elif query.data == 'manual_input':
        await query.edit_message_text("✍️ Fitur Input Manual\n\nMasukkan nama kontak:")
        
    elif query.data == 'file_info':
        await query.edit_message_text("ℹ️ Fitur Info File\n\nKirim file untuk melihat informasi detail")
        
    # Conversion Features Handlers  
    elif query.data == 'conv_txt_to_vcf':
        await query.edit_message_text("📝➡️📇 TXT ke VCF\n\nKirim file TXT yang berisi daftar kontak untuk dikonversi ke VCF")
        
    elif query.data == 'conv_split_txt':
        await query.edit_message_text("📝✂️ Split TXT\n\nKirim file TXT yang ingin dipecah menjadi beberapa file kecil")
        
    elif query.data == 'conv_vcf_to_txt':
        await query.edit_message_text("📇➡️📝 VCF ke TXT\n\nKirim file VCF untuk dikonversi ke format TXT")
        
    elif query.data == 'conv_xls_to_vcf':
        await query.edit_message_text("📊➡️📇 XLS ke VCF\n\nKirim file Excel (.xls/.xlsx) untuk dikonversi ke VCF")
        
    # Back to main menu
    elif query.data == 'back_to_main':
        custom_data = get_customization_data()
        welcome_message = custom_data.get("welcome_message", "Selamat datang! Silakan pilih opsi:")
        await query.edit_message_text(welcome_message, reply_markup=main_menu())
        
    # Premium info
    elif query.data == 'premium':
        prices_data = get_prices_data()
        payment_info = get_customization_data()
        
        price_text = "💎 Informasi Premium:\n\n"
        for duration, price in prices_data.items():
            price_text += f"• {duration}: {price}\n"
        
        price_text += f"\n💳 Metode Pembayaran: {payment_info.get('payment_method', 'Belum diset')}"
        if payment_info.get('qr_code_url'):
            price_text += f"\n📱 QR Code: {payment_info.get('qr_code_url')}"
            
        await query.edit_message_text(price_text)
        
    else:
        # Default fallback
        await query.edit_message_text("Maaf, fitur ini sedang dalam pengembangan. Silakan pilih menu lain.", reply_markup=main_menu())
