from telegram import Update
from telegram.ext import ContextTypes
from .menus import (
    main_menu, features_menu, conversion_menu, file_tools_menu,
    premium_menu, admin_menu, cancel_button, back_button,
    file_type_menu, duplicate_action_menu
)
from utils.user_manager import user_manager
from utils.logger import log_activity
from utils.caching import get_customization_data
from config import ADMIN_ID
import os

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    
    # Log activity
    log_activity(user_id, f"Button: {callback_data}")
    
    # Handle different callback data
    if callback_data == 'trial':
        await handle_trial(update, context)
    elif callback_data == 'premium':
        await handle_premium(update, context)
    elif callback_data == 'info':
        await handle_info(update, context)
    elif callback_data == 'conversion_features':
        await handle_conversion_features(update, context)
    elif callback_data == 'file_tools':
        await handle_file_tools(update, context)
    elif callback_data == 'manual_input':
        await handle_manual_input(update, context)
    elif callback_data.startswith('conv_'):
        await handle_conversion_option(update, context)
    elif callback_data.startswith('premium_'):
        await handle_premium_selection(update, context)
    elif callback_data.startswith('admin_'):
        await handle_admin_option(update, context)
    elif callback_data == 'cancel':
        await handle_cancel(update, context)
    elif callback_data.startswith('back_'):
        await handle_back(update, context)
    else:
        await handle_file_tools_callback(update, context)

async def handle_trial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle trial activation"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    # Check if user already has trial
    access_info = user_manager.check_access(user_id)
    if access_info["has_access"]:
        await query.edit_message_text(
            "✅ Anda sudah memiliki akses aktif!\n\n"
            f"Status: {access_info['status']}\n"
            "Silakan gunakan fitur-fitur bot.",
            reply_markup=features_menu()
        )
        return
    
    # Activate trial
    success = user_manager.activate_trial(user_id)
    if success:
        await query.edit_message_text(
            "🧪 Trial berhasil diaktifkan!\n\n"
            "⏰ Durasi: 1 jam\n"
            "✅ Akses ke semua fitur\n\n"
            "Silakan pilih fitur yang ingin digunakan:",
            reply_markup=features_menu()
        )
    else:
        await query.edit_message_text(
            "❌ Trial sudah pernah digunakan!\n\n"
            "Silakan pilih opsi Premium untuk akses penuh.",
            reply_markup=main_menu()
        )

async def handle_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle premium menu"""
    query = update.callback_query
    custom_data = get_customization_data()
    
    message = "🔐 PREMIUM SUBSCRIPTION\n\n"
    message += "Pilih paket yang sesuai:\n\n"
    
    prices = custom_data.get("prices", {})
    for plan, price in prices.items():
        plan_name = plan.replace("_", " ").title()
        message += f"• {plan_name}: Rp {price:,}\n"
    
    message += "\n💳 Metode Pembayaran:\n"
    message += f"• {custom_data.get('payment_method', 'Transfer Bank')}\n\n"
    message += "Silakan pilih paket:"
    
    await query.edit_message_text(message, reply_markup=premium_menu())

async def handle_premium_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle premium plan selection"""
    query = update.callback_query
    plan = query.data.replace('premium_', '')
    
    custom_data = get_customization_data()
    prices = custom_data.get("prices", {})
    price = prices.get(plan, 0)
    
    message = f"🔐 PREMIUM {plan.replace('_', ' ').upper()}\n\n"
    message += f"💰 Harga: Rp {price:,}\n"
    message += f"💳 Metode: {custom_data.get('payment_method', 'Transfer Bank')}\n\n"
    
    # Check if QR code exists
    qr_path = custom_data.get("qr_code_path")
    if qr_path and os.path.exists(qr_path):
        message += "📱 Silakan scan QR code di bawah ini untuk pembayaran:\n\n"
        message += "Setelah pembayaran, hubungi admin untuk aktivasi."
        
        # Send QR code
        with open(qr_path, 'rb') as qr_file:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_file,
                caption=message,
                reply_markup=back_button('premium')
            )
        await query.delete_message()
    else:
        message += "📞 Hubungi admin untuk informasi pembayaran.\n\n"
        message += "Admin ID: " + str(ADMIN_ID)
        await query.edit_message_text(message, reply_markup=back_button('premium'))

async def handle_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle info bot"""
    query = update.callback_query
    
    message = "ℹ️ INFO BOT\n\n"
    message += "🤖 Bot Konversi Kontak Telegram\n\n"
    message += "📁 Fitur Utama:\n"
    message += "• Konversi TXT ➝ VCF\n"
    message += "• Split file TXT\n"
    message += "• Ekstrak nomor dari VCF\n"
    message += "• Konversi XLS ➝ VCF\n"
    message += "• Tools manipulasi file\n\n"
    message += "👨‍💻 Developer: Admin\n"
    message += "📧 Support: Hubungi Admin\n\n"
    message += "🔐 Akses:\n"
    message += "• Trial: 1 jam gratis\n"
    message += "• Premium: Akses penuh"
    
    await query.edit_message_text(message, reply_markup=back_button('back_to_main'))

async def handle_conversion_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle conversion features menu"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    # Check access
    access_info = user_manager.check_access(user_id)
    if not access_info["has_access"]:
        await query.edit_message_text(
            "❌ Akses ditolak!\n\n"
            f"Alasan: {access_info['reason']}\n\n"
            "Silakan pilih Trial atau Premium untuk mengakses fitur.",
            reply_markup=main_menu()
        )
        return
    
    await query.edit_message_text(
        "📁 FITUR KONVERSI\n\n"
        "Pilih jenis konversi yang diinginkan:",
        reply_markup=conversion_menu()
    )

async def handle_file_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file tools menu"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    # Check access
    access_info = user_manager.check_access(user_id)
    if not access_info["has_access"]:
        await query.edit_message_text(
            "❌ Akses ditolak!\n\n"
            f"Alasan: {access_info['reason']}\n\n"
            "Silakan pilih Trial atau Premium untuk mengakses fitur.",
            reply_markup=main_menu()
        )
        return
    
    await query.edit_message_text(
        "🛠️ FILE TOOLS\n\n"
        "Pilih tool yang ingin digunakan:",
        reply_markup=file_tools_menu()
    )

async def handle_manual_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle manual input menu"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    # Check access
    access_info = user_manager.check_access(user_id)
    if not access_info["has_access"]:
        await query.edit_message_text(
            "❌ Akses ditolak!\n\n"
            f"Alasan: {access_info['reason']}\n\n"
            "Silakan pilih Trial atau Premium untuk mengakses fitur.",
            reply_markup=main_menu()
        )
        return
    
    # Start manual input conversation
    context.user_data['manual_input_state'] = 'waiting_name'
    await query.edit_message_text(
        "🧾 INPUT MANUAL\n\n"
        "Silakan ketik nama kontak:",
        reply_markup=cancel_button()
    )

async def handle_conversion_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle conversion option selection"""
    query = update.callback_query
    conversion_type = query.data.replace('conv_', '')
    
    user_id = update.effective_user.id
    access_info = user_manager.check_access(user_id)
    if not access_info["has_access"]:
        await query.edit_message_text(
            "❌ Akses ditolak!\n\n"
            f"Alasan: {access_info['reason']}\n\n"
            "Silakan pilih Trial atau Premium untuk mengakses fitur.",
            reply_markup=main_menu()
        )
        return
    
    # Set conversion type in context
    context.user_data['conversion_type'] = conversion_type
    
    if conversion_type == 'txt_to_vcf':
        await query.edit_message_text(
            "📂 TXT ➝ VCF (Format TUTOR KIKS)\n\n"
            "Silakan kirim file .txt yang berisi nomor telepon (satu nomor per baris).\n\n"
            "Setelah file diterima, bot akan meminta:\n"
            "• Nama file dasar\n"
            "• Nama kontak dasar\n"
            "• Jumlah kontak per file\n"
            "• Urutan awal file",
            reply_markup=cancel_button()
        )
    elif conversion_type == 'split_txt':
        await query.edit_message_text(
            "✂️ TXT ➝ TXT (Split)\n\n"
            "Silakan kirim file .txt yang ingin dibagi.\n\n"
            "Bot akan meminta jumlah baris per file.",
            reply_markup=cancel_button()
        )
    elif conversion_type == 'vcf_to_txt':
        await query.edit_message_text(
            "📤 VCF ➝ TXT\n\n"
            "Silakan kirim file .vcf yang ingin diekstrak nomornya.\n\n"
            "Bot akan mengekstrak semua nomor telepon dan menyimpannya dalam file .txt.",
            reply_markup=cancel_button()
        )
    elif conversion_type == 'xls_to_vcf':
        await query.edit_message_text(
            "📊 XLS ➝ VCF\n\n"
            "Silakan kirim file .xls atau .xlsx.\n\n"
            "Bot akan membaca:\n"
            "• Kolom A = Nama\n"
            "• Kolom B = Nomor\n\n"
            "Dan mengkonversi ke format VCF.",
            reply_markup=cancel_button()
        )

async def handle_admin_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin options"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    # Check if user is admin
    if user_id != ADMIN_ID:
        await query.edit_message_text(
            "❌ Anda tidak memiliki izin untuk mengakses menu admin!",
            reply_markup=back_button('back_to_main')
        )
        return
    
    admin_option = query.data.replace('admin_', '')
    
    if admin_option == 'broadcast':
        await query.edit_message_text(
            "📢 BROADCAST MESSAGE\n\n"
            "Silakan ketik pesan yang ingin disiarkan ke semua user:",
            reply_markup=cancel_button()
        )
        context.user_data['admin_state'] = 'broadcast'
    elif admin_option == 'payment':
        await query.edit_message_text(
            "💳 GANTI METODE PEMBAYARAN\n\n"
            "Silakan kirim QR code atau ketik metode pembayaran baru:",
            reply_markup=cancel_button()
        )
        context.user_data['admin_state'] = 'payment'
    elif admin_option == 'prices':
        await query.edit_message_text(
            "🛠️ ATUR HARGA PREMIUM\n\n"
            "Silakan ketik harga dalam format:\n"
            "1_hari:5000\n"
            "7_hari:25000\n"
            "30_hari:75000\n"
            "lifetime:200000",
            reply_markup=cancel_button()
        )
        context.user_data['admin_state'] = 'prices'
    elif admin_option == 'users':
        await handle_admin_users(update, context)
    elif admin_option == 'logs':
        await handle_admin_logs(update, context)
    else:
        await query.edit_message_text(
            "🛠️ ADMIN PANEL\n\n"
            "Fitur sedang dalam pengembangan.",
            reply_markup=admin_menu()
        )

async def handle_admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin users list"""
    query = update.callback_query
    
    users = user_manager.get_all_users()
    stats = user_manager.get_user_stats()
    
    message = "👥 DAFTAR USER\n\n"
    message += f"📊 Statistik:\n"
    message += f"• Total: {stats['total']}\n"
    message += f"• Trial: {stats['trial']}\n"
    message += f"• Premium: {stats['premium']}\n"
    message += f"• Expired: {stats['expired']}\n\n"
    
    if users:
        message += "📋 Daftar User:\n"
        for user in users[:10]:  # Show first 10 users
            status_emoji = "✅" if user['has_access'] else "❌"
            message += f"{status_emoji} ID: {user['user_id']}\n"
            message += f"   Status: {user['status']}\n"
            if user.get('expires'):
                message += f"   Expires: {user['expires'][:19]}\n"
            message += "\n"
        
        if len(users) > 10:
            message += f"... dan {len(users) - 10} user lainnya"
    else:
        message += "Belum ada user terdaftar."
    
    await query.edit_message_text(message, reply_markup=admin_menu())

async def handle_admin_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin logs"""
    query = update.callback_query
    
    from utils.logger import get_recent_logs
    
    logs = get_recent_logs(20)
    if logs:
        message = "📋 LOG AKTIVITAS (20 terakhir)\n\n"
        message += logs
    else:
        message = "📋 LOG AKTIVITAS\n\nBelum ada aktivitas yang tercatat."
    
    await query.edit_message_text(message, reply_markup=admin_menu())

async def handle_file_tools_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file tools callbacks"""
    query = update.callback_query
    callback_data = query.data
    
    user_id = update.effective_user.id
    access_info = user_manager.check_access(user_id)
    if not access_info["has_access"]:
        await query.edit_message_text(
            "❌ Akses ditolak!\n\n"
            f"Alasan: {access_info['reason']}\n\n"
            "Silakan pilih Trial atau Premium untuk mengakses fitur.",
            reply_markup=main_menu()
        )
        return
    
    if callback_data == 'merge_files':
        await query.edit_message_text(
            "📎 GABUNGKAN FILE\n\n"
            "Silakan kirim beberapa file .txt atau .vcf yang ingin digabungkan.\n\n"
            "Setelah semua file dikirim, ketik /done untuk melanjutkan.",
            reply_markup=cancel_button()
        )
        context.user_data['merge_files'] = []
    elif callback_data == 'check_duplicates':
        await query.edit_message_text(
            "🔍 CEK DUPLIKAT\n\n"
            "Silakan kirim file .txt atau .vcf yang ingin dicek duplikatnya.",
            reply_markup=cancel_button()
        )
    elif callback_data == 'add_contact':
        await query.edit_message_text(
            "➕ TAMBAH KONTAK\n\n"
            "Silakan kirim file .txt atau .vcf yang ingin ditambahkan kontaknya.",
            reply_markup=cancel_button()
        )
    elif callback_data == 'rename_file':
        await query.edit_message_text(
            "✏️ RENAME FILE\n\n"
            "Silakan kirim file yang ingin diubah namanya.",
            reply_markup=cancel_button()
        )
    elif callback_data == 'delete_number':
        await query.edit_message_text(
            "❌ HAPUS NOMOR\n\n"
            "Silakan kirim file .txt atau .vcf yang ingin dihapus nomornya.",
            reply_markup=cancel_button()
        )
    elif callback_data == 'split_file_tool':
        await query.edit_message_text(
            "✂️ PECAH FILE\n\n"
            "Silakan kirim file besar yang ingin dipecah.",
            reply_markup=cancel_button()
        )

async def handle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle cancel button"""
    query = update.callback_query
    
    # Clear user data
    context.user_data.clear()
    
    await query.edit_message_text(
        "❌ Operasi dibatalkan.\n\n"
        "Silakan pilih menu lain:",
        reply_markup=main_menu()
    )

async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle back button"""
    query = update.callback_query
    callback_data = query.data
    
    if callback_data == 'back_to_main':
        await query.edit_message_text(
            "🔐 SISTEM AKSES USER\n\n"
            "Silakan pilih opsi:",
            reply_markup=main_menu()
        )
    elif callback_data == 'back_to_features':
        await query.edit_message_text(
            "📁 FITUR UTAMA\n\n"
            "Silakan pilih kategori fitur:",
            reply_markup=features_menu()
        )
    elif callback_data == 'back_to_file_tools':
        await query.edit_message_text(
            "🛠️ FILE TOOLS\n\n"
            "Pilih tool yang ingin digunakan:",
            reply_markup=file_tools_menu()
        )
    elif callback_data == 'premium':
        await handle_premium(update, context)
