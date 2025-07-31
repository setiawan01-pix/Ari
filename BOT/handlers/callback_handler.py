from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from utils.caching import get_user_data, update_user_data, get_customization_data
import json

from handlers.file_handler import ASK_FILENAME, ASK_CONTACTS_PER_FILE as ASK_LINES_PER_FILE
from .menus import file_tools_menu, conversion_menu

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    user_data = get_user_data()

    if query.data == 'trial':
        # Check if user already has active trial
        if user_id in user_data and user_data[user_id].get("status") == "trial":
            expire_time = datetime.fromisoformat(user_data[user_id]["expire_time"])
            if datetime.now() < expire_time:
                remaining = expire_time - datetime.now()
                hours = int(remaining.total_seconds() // 3600)
                minutes = int((remaining.total_seconds() % 3600) // 60)
                await query.edit_message_text(text=f"🧪 Trial sudah aktif!\nSisa waktu: {hours}j {minutes}m")
                return
        
        # Start new trial
        user_data[user_id] = {
            "status": "trial",
            "start_time": str(datetime.now()),
            "expire_time": str(datetime.now() + timedelta(hours=1))
        }
        update_user_data(user_data)
        
        trial_text = """🧪 TRIAL AKTIVASI BERHASIL!

⏰ Durasi: 1 jam
🎯 Akses: Semua fitur
⚡ Mulai: Sekarang

📂 Fitur yang tersedia:
• TXT ➝ VCF conversion
• File tools lengkap
• Split & merge files

Trial akan otomatis expired dalam 1 jam."""
        
        keyboard = [[InlineKeyboardButton("📁 Mulai Konversi", callback_data='conversion_features')],
                   [InlineKeyboardButton("🔙 Menu Utama", callback_data='back_to_main')]]
        
        await query.edit_message_text(text=trial_text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'premium':
        # Display premium pricing and payment info
        try:
            with open('BOT/prices.json', 'r') as f:
                prices = json.load(f)
            
            custom_data = get_customization_data()
            payment_method = custom_data.get("payment_method", "Transfer Bank")
            qr_url = custom_data.get("qr_code_url", "")
            
            premium_text = "🔐 PREMIUM (Berbayar)\n\n💰 Harga:\n"
            for duration, price in prices.items():
                if duration == "lifetime":
                    premium_text += f"• Lifetime: Rp {price:,}\n"
                else:
                    premium_text += f"• {duration} hari: Rp {price:,}\n"
            
            premium_text += f"\n💳 Metode Pembayaran: {payment_method}\n"
            premium_text += "📞 Hubungi admin untuk aktivasi premium\n"
            premium_text += "⚡ Akses unlimited semua fitur"
            
            keyboard = []
            if qr_url and qr_url != "https://example.com/qr.png":
                keyboard.append([InlineKeyboardButton("📱 Lihat QR Code", url=qr_url)])
            keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main')])
            
            await query.edit_message_text(text=premium_text, reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception as e:
            await query.edit_message_text(text="Terjadi kesalahan saat memuat informasi premium.")

    elif query.data == 'info':
        info_text = """ℹ️ INFO BOT
        
🤖 Bot Konversi Kontak TUTOR KIKS
📂 Fitur Utama:
• TXT ➝ VCF (Format khusus)
• Split file TXT
• File tools lengkap
• Merge, duplicate check, dll

🔄 Alur TXT ➝ VCF:
1. Upload file .txt (nomor per baris)
2. Bot tanya parameter via tombol
3. Terima file VCF siap pakai

🧪 Trial: 1 jam gratis
🔐 Premium: Akses unlimited

Dikembangkan untuk TUTOR KIKS"""
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main')]]
        await query.edit_message_text(text=info_text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'back_to_main':
        from utils.access_control import get_user_status
        from .menus import main_menu
        user_status = get_user_status(query.from_user.id)
        
        custom_data = get_customization_data()
        base_welcome = custom_data.get("welcome_message", "🔐 SISTEM AKSES USER💬")
        status_message = f"{base_welcome}\n\n"
        
        if user_status == "trial":
            user_data = get_user_data()
            expire_time = datetime.fromisoformat(user_data[str(query.from_user.id)]["expire_time"])
            remaining = expire_time - datetime.now()
            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)
            status_message += f"🧪 Trial aktif - sisa {hours}j {minutes}m\n"
        elif user_status == "premium":
            status_message += "🔐 Premium aktif\n"
        elif user_status == "expired":
            status_message += "⏰ Trial expired - akses terbatas\n"
        else:
            status_message += "ℹ️ Akses belum aktif\n"
        
        status_message += "\n📂 TXT ➝ VCF (Format TUTOR KIKS)\nAlur: Upload file .txt → Bot tanya parameter → Kirim file VCF"
        
        await query.edit_message_text(text=status_message, reply_markup=main_menu(user_status))

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
    
    elif query.data == 'conv_txt_to_vcf':
        await query.edit_message_text("📁 TXT ➝ VCF Converter\n\n📤 Upload file TXT Anda (nomor per baris)\nSetelah upload, bot akan meminta parameter konversi.")
        return None  # Wait for file upload
    
    elif query.data == 'start_txt_vcf':
        await query.edit_message_text("📝 Masukkan nama file dasar:\n(Contoh: OLXX)")
        return ASK_FILENAME
    
    elif query.data == 'start_split_txt':
        await query.edit_message_text("✂️ Masukkan jumlah baris per file:")
        return ASK_LINES_PER_FILE
