#!/usr/bin/env python3
"""
Telegram Bot Script dengan Fitur Admin dan Langganan
Bot Telegram lengkap dengan sistem admin, langganan, dan notifikasi otomatis
"""

import logging
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler
from datetime import datetime, timedelta
from typing import Dict, Any

# Import modul custom
from config import config
from database import db_manager
from admin_handlers import admin_manager, WAITING_USER_ID, WAITING_DURATION
from notification_system import NotificationSystem
from tools import conversion_tools, text_tools, datetime_tools, json_tools, calculator_tools, url_tools

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token dari config
BOT_TOKEN = config.token

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk command /start"""
    user = update.effective_user
    
    # Tambah user ke database
    db_manager.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    welcome_message = f"""
🤖 **Selamat datang di Bot Telegram Premium!**

Halo {user.first_name}! 👋

Saya adalah bot lengkap dengan fitur admin, sistem langganan, dan tools konversi.

📋 **Perintah Utama:**
• `/status` - Cek status langganan Anda
• `/tools` - Menu tools dan konversi
• `/help` - Bantuan lengkap
• `/contact` - Hubungi admin

🛠️ **Tools Cepat:**
• `calc 2 + 2` - Kalkulator
• `base64 teks` - Encode Base64
• `md5 teks` - Generate MD5

💎 **Fitur Premium:**
• Sistem langganan otomatis
• Notifikasi perpanjangan
• Tools konversi lengkap
• Panel admin terintegrasi

Silakan gunakan command di atas untuk mulai!
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk command /help"""
    help_text = """
📚 **BANTUAN BOT TELEGRAM**

🔹 **Perintah Dasar:**
• `/start` - Pesan selamat datang
• `/help` - Menampilkan bantuan ini
• `/info` - Informasi bot
• `/ping` - Test koneksi

🔹 **Perintah User:**
• `/status` - Cek status langganan Anda
• `/contact` - Hubungi admin
• `/tools` - Menu tools dan konversi

🔹 **Perintah Admin:**
• `/admin` - Panel admin (hanya untuk admin)

🔹 **Tools & Konversi:**
• `calc 2 + 2` - Kalkulator
• `base64 teks` - Encode ke Base64
• `decode base64string` - Decode dari Base64
• `md5 teks` - Generate MD5 hash
• `sha256 teks` - Generate SHA256 hash

🔹 **Fitur Premium:**
• Sistem langganan otomatis
• Notifikasi perpanjangan
• Tools konversi lengkap
• Panel admin terintegrasi

🔧 **Cara menggunakan:**
Ketik perintah yang diinginkan atau gunakan menu tools untuk fitur konversi.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk command /info"""
    info_text = """
ℹ️ Informasi Bot

🤖 Nama: Telegram Bot
📅 Dibuat dengan: python-telegram-bot
🐍 Bahasa: Python 3
📊 Status: Aktif

💡 Bot ini dibuat sebagai contoh implementasi dasar bot Telegram menggunakan Python.
    """
    await update.message.reply_text(info_text)

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk command /ping"""
    await update.message.reply_text("🏓 Pong! Bot berjalan dengan baik!")

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk pesan teks biasa"""
    user_message = update.message.text
    user = update.effective_user
    
    # Cek status langganan user
    status = db_manager.get_subscription_status(user.id)
    
    # Respon sederhana berdasarkan pesan
    if user_message.lower() in ['halo', 'hello', 'hi', 'hai']:
        response = f"Halo {user.first_name}! 👋 Senang bertemu dengan Anda!"
    elif user_message.lower() in ['terima kasih', 'thanks', 'thank you']:
        response = "Sama-sama! 😊 Senang bisa membantu!"
    elif '?' in user_message:
        response = "Pertanyaan yang menarik! 🤔 Silakan gunakan /help untuk melihat perintah yang tersedia."
    else:
        # Cek apakah user memiliki langganan aktif
        if status['status'] == 'active':
            response = f"Pesan Anda: '{user_message}'\n\n✅ Anda memiliki akses premium!\nGunakan /tools untuk fitur konversi lengkap."
        elif status['status'] == 'expired':
            response = f"Pesan Anda: '{user_message}'\n\n❌ Langganan Anda sudah habis.\nGunakan /contact untuk menghubungi admin."
        else:
            response = f"Pesan Anda: '{user_message}'\n\n🆓 Anda menggunakan akun gratis.\nGunakan /contact untuk upgrade ke premium."
    
    await update.message.reply_text(response)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk error"""
    logger.error(f"Exception while handling an update: {context.error}")
    if update and hasattr(update, 'message'):
        await update.message.reply_text("Maaf, terjadi kesalahan. Silakan coba lagi nanti.")

# ==================== ADMIN COMMANDS ====================

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command untuk admin panel"""
    await admin_manager.admin_menu(update, context)

async def admin_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk callback admin"""
    await admin_manager.admin_callback(update, context)

async def handle_admin_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle input user ID untuk admin"""
    return await admin_manager.handle_user_id_input(update, context)

async def handle_admin_duration_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle callback durasi untuk admin"""
    return await admin_manager.handle_duration_callback(update, context)

# ==================== USER COMMANDS ====================

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command untuk cek status langganan user"""
    user_id = update.effective_user.id
    
    # Tambah user ke database jika belum ada
    db_manager.add_user(
        user_id=user_id,
        username=update.effective_user.username,
        first_name=update.effective_user.first_name,
        last_name=update.effective_user.last_name
    )
    
    # Cek status langganan
    status = db_manager.get_subscription_status(user_id)
    
    status_text = f"📊 **STATUS LANGGANAN ANDA**\n\n"
    status_text += f"👤 **Nama:** {update.effective_user.first_name}\n"
    status_text += f"🆔 **ID:** `{user_id}`\n"
    status_text += f"📅 **Status:** {status['message']}\n\n"
    
    if status['status'] == 'active':
        status_text += "✅ **Akses:** Fitur premium tersedia\n"
        status_text += f"⏰ **Tersisa:** {status['days_remaining']} hari\n"
        status_text += f"📅 **Expired:** {status['expired_date']:%d/%m/%Y}\n"
    elif status['status'] == 'expired':
        status_text += "❌ **Akses:** Fitur premium dibatasi\n"
        status_text += f"⏰ **Habis:** {status['days_expired']} hari yang lalu\n"
        status_text += "🔁 **Solusi:** Hubungi admin untuk perpanjangan\n"
    elif status['status'] == 'free':
        status_text += "🆓 **Akses:** Fitur dasar tersedia\n"
        status_text += "💎 **Upgrade:** Hubungi admin untuk fitur premium\n"
    
    status_text += "\n💬 Gunakan /contact untuk menghubungi admin"
    
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command untuk menghubungi admin"""
    contact_text = (
        "📞 **HUBUNGI ADMIN**\n\n"
        "Untuk pertanyaan, bantuan, atau perpanjangan langganan:\n\n"
        "👤 **Admin:** @admin_username\n"
        "📧 **Email:** admin@example.com\n"
        "💬 **Telegram:** https://t.me/admin_username\n\n"
        "⏰ **Jam Operasional:**\n"
        "Senin - Jumat: 09:00 - 17:00 WIB\n"
        "Sabtu: 09:00 - 15:00 WIB\n\n"
        "📝 **Informasi yang perlu disiapkan:**\n"
        "• ID Telegram Anda\n"
        "• Jenis langganan yang diinginkan\n"
        "• Durasi langganan\n\n"
        "Terima kasih! 🙏"
    )
    
    await update.message.reply_text(contact_text, parse_mode='Markdown')

# ==================== TOOLS COMMANDS ====================

async def tools_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menu tools dan konversi"""
    keyboard = [
        [InlineKeyboardButton("🔄 Konversi", callback_data="tools_convert")],
        [InlineKeyboardButton("📝 Text Tools", callback_data="tools_text")],
        [InlineKeyboardButton("🕐 DateTime", callback_data="tools_datetime")],
        [InlineKeyboardButton("📊 JSON Tools", callback_data="tools_json")],
        [InlineKeyboardButton("🧮 Kalkulator", callback_data="tools_calc")],
        [InlineKeyboardButton("🔗 URL Tools", callback_data="tools_url")],
        [InlineKeyboardButton("❌ Tutup", callback_data="tools_close")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🛠️ **TOOLS & KONVERSI**\n\n"
        "Silakan pilih kategori tools yang diinginkan:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def tools_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk callback tools"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "tools_convert":
        await show_conversion_tools(query, context)
    elif query.data == "tools_text":
        await show_text_tools(query, context)
    elif query.data == "tools_datetime":
        await show_datetime_tools(query, context)
    elif query.data == "tools_json":
        await show_json_tools(query, context)
    elif query.data == "tools_calc":
        await show_calculator_tools(query, context)
    elif query.data == "tools_url":
        await show_url_tools(query, context)
    elif query.data == "tools_close":
        await query.edit_message_text("✅ Tools menu ditutup")

async def show_conversion_tools(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tampilkan menu konversi"""
    keyboard = [
        [InlineKeyboardButton("🔤 Text ↔ Base64", callback_data="conv_base64")],
        [InlineKeyboardButton("🔐 Text → MD5", callback_data="conv_md5")],
        [InlineKeyboardButton("🔐 Text → SHA256", callback_data="conv_sha256")],
        [InlineKeyboardButton("🌡️ Celsius ↔ Fahrenheit", callback_data="conv_temp")],
        [InlineKeyboardButton("📏 KM ↔ Miles", callback_data="conv_distance")],
        [InlineKeyboardButton("⚖️ KG ↔ Pounds", callback_data="conv_weight")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="tools_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🔄 **KONVERSI**\n\n"
        "Pilih jenis konversi yang diinginkan:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_text_tools(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tampilkan menu text tools"""
    keyboard = [
        [InlineKeyboardButton("📊 Hitung Karakter", callback_data="text_count")],
        [InlineKeyboardButton("🔄 Balik Teks", callback_data="text_reverse")],
        [InlineKeyboardButton("🔤 Uppercase", callback_data="text_upper")],
        [InlineKeyboardButton("🔤 Lowercase", callback_data="text_lower")],
        [InlineKeyboardButton("🔤 Title Case", callback_data="text_title")],
        [InlineKeyboardButton("🚫 Hapus Spasi", callback_data="text_nospace")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="tools_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📝 **TEXT TOOLS**\n\n"
        "Pilih tool teks yang diinginkan:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_datetime_tools(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tampilkan menu datetime tools"""
    current_time = datetime_tools.get_current_time()
    
    time_text = "🕐 **WAKTU SAAT INI**\n\n"
    time_text += f"📅 **Tanggal:** {current_time['date']}\n"
    time_text += f"⏰ **Waktu:** {current_time['time']}\n"
    time_text += f"📊 **Timestamp:** {current_time['timestamp']}\n"
    time_text += f"🌐 **ISO:** {current_time['iso']}\n"
    time_text += f"📝 **Format:** {current_time['formatted']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data="tools_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        time_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_json_tools(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tampilkan menu JSON tools"""
    keyboard = [
        [InlineKeyboardButton("📝 Format JSON", callback_data="json_format")],
        [InlineKeyboardButton("📦 Minify JSON", callback_data="json_minify")],
        [InlineKeyboardButton("✅ Validasi JSON", callback_data="json_validate")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="tools_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📊 **JSON TOOLS**\n\n"
        "Pilih tool JSON yang diinginkan:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_calculator_tools(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tampilkan menu calculator"""
    keyboard = [
        [InlineKeyboardButton("🔙 Kembali", callback_data="tools_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🧮 **KALKULATOR**\n\n"
        "Untuk menggunakan kalkulator, ketik:\n"
        "`calc 2 + 2` atau `calc 10 * 5`\n\n"
        "**Operasi yang didukung:**\n"
        "• Penjumlahan (+)\n"
        "• Pengurangan (-)\n"
        "• Perkalian (*)\n"
        "• Pembagian (/)\n"
        "• Pangkat (**)\n"
        "• Kurung untuk prioritas\n\n"
        "**Contoh:**\n"
        "• `calc 15 + 25`\n"
        "• `calc 100 / 4`\n"
        "• `calc (2 + 3) * 4`",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_url_tools(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tampilkan menu URL tools"""
    keyboard = [
        [InlineKeyboardButton("🔗 Ekstrak URL", callback_data="url_extract")],
        [InlineKeyboardButton("✅ Validasi URL", callback_data="url_validate")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="tools_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🔗 **URL TOOLS**\n\n"
        "Pilih tool URL yang diinginkan:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ==================== MESSAGE HANDLERS ====================

async def handle_calculator_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle pesan kalkulator"""
    message_text = update.message.text.lower()
    
    if message_text.startswith('calc '):
        expression = message_text[5:]  # Hapus 'calc '
        result = calculator_tools.calculate(expression)
        
        await update.message.reply_text(
            f"🧮 **KALKULATOR**\n\n"
            f"📝 **Ekspresi:** `{expression}`\n"
            f"📊 **Hasil:** `{result}`",
            parse_mode='Markdown'
        )

async def handle_conversion_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle pesan konversi"""
    message_text = update.message.text.lower()
    
    if message_text.startswith('base64 '):
        text = message_text[7:]  # Hapus 'base64 '
        result = conversion_tools.text_to_base64(text)
        await update.message.reply_text(
            f"🔤 **BASE64 ENCODE**\n\n"
            f"📝 **Teks:** `{text}`\n"
            f"🔐 **Base64:** `{result}`",
            parse_mode='Markdown'
        )
    
    elif message_text.startswith('decode '):
        base64_text = message_text[7:]  # Hapus 'decode '
        result = conversion_tools.base64_to_text(base64_text)
        await update.message.reply_text(
            f"🔤 **BASE64 DECODE**\n\n"
            f"🔐 **Base64:** `{base64_text}`\n"
            f"📝 **Teks:** `{result}`",
            parse_mode='Markdown'
        )
    
    elif message_text.startswith('md5 '):
        text = message_text[4:]  # Hapus 'md5 '
        result = conversion_tools.text_to_md5(text)
        await update.message.reply_text(
            f"🔐 **MD5 HASH**\n\n"
            f"📝 **Teks:** `{text}`\n"
            f"🔐 **MD5:** `{result}`",
            parse_mode='Markdown'
        )
    
    elif message_text.startswith('sha256 '):
        text = message_text[7:]  # Hapus 'sha256 '
        result = conversion_tools.text_to_sha256(text)
        await update.message.reply_text(
            f"🔐 **SHA256 HASH**\n\n"
            f"📝 **Teks:** `{text}`\n"
            f"🔐 **SHA256:** `{result}`",
            parse_mode='Markdown'
        )

def main() -> None:
    """Fungsi utama untuk menjalankan bot"""
    # Cek token bot
    if not config.is_token_set():
        print("❌ Error: Token bot belum diset!")
        print("🔧 Cara mengatur token:")
        print("1. Set environment variable: export BOT_TOKEN='your_token_here'")
        print("2. Atau edit file config.py")
        return
    
    # Buat aplikasi bot
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ==================== COMMAND HANDLERS ====================
    
    # Command dasar
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("ping", ping_command))
    
    # Command user
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("contact", contact_command))
    application.add_handler(CommandHandler("tools", tools_command))
    
    # Command admin
    application.add_handler(CommandHandler("admin", admin_command))
    
    # ==================== CONVERSATION HANDLERS ====================
    
    # Admin conversation untuk perpanjang langganan
    admin_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_manager.start_extend_subscription, pattern="^admin_extend$")],
        states={
            WAITING_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_user_input)],
            WAITING_DURATION: [CallbackQueryHandler(handle_admin_duration_callback)]
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(admin_conv_handler)
    
    # ==================== CALLBACK HANDLERS ====================
    
    # Admin callbacks
    application.add_handler(CallbackQueryHandler(admin_callback_handler, pattern="^admin_"))
    
    # Tools callbacks
    application.add_handler(CallbackQueryHandler(tools_callback_handler, pattern="^tools_"))
    
    # ==================== MESSAGE HANDLERS ====================
    
    # Handler untuk pesan kalkulator dan konversi
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r'^(calc|base64|decode|md5|sha256)\s+'),
        lambda u, c: asyncio.create_task(handle_calculator_message(u, c)) or asyncio.create_task(handle_conversion_message(u, c))
    ))
    
    # Handler untuk pesan teks biasa
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    
    # ==================== ERROR HANDLER ====================
    
    application.add_error_handler(error_handler)
    
    # ==================== NOTIFICATION SYSTEM ====================
    
    # Inisialisasi sistem notifikasi
    global notification_system
    notification_system = NotificationSystem(application.bot)
    
    # ==================== STARTUP TASKS ====================
    
    async def startup_tasks():
        """Task yang dijalankan saat bot start"""
        try:
            # Mulai sistem notifikasi
            await notification_system.start_notification_service()
            logger.info("✅ Sistem notifikasi berhasil dimulai")
            
            # Kirim notifikasi ke admin
            for admin_id in config.admin_ids:
                await notification_system.send_admin_notification(
                    admin_id,
                    "🚀 Bot telah berhasil dijalankan!\n"
                    "📊 Sistem notifikasi otomatis aktif\n"
                    "👑 Admin panel tersedia dengan command /admin"
                )
            
        except Exception as e:
            logger.error(f"Error dalam startup tasks: {e}")
    
    # Jalankan startup tasks
    asyncio.create_task(startup_tasks())
    
    # ==================== SHUTDOWN HANDLER ====================
    
    async def shutdown_handler():
        """Handler untuk shutdown bot"""
        try:
            # Hentikan sistem notifikasi
            if notification_system:
                await notification_system.stop_notification_service()
            
            # Kirim notifikasi ke admin
            for admin_id in config.admin_ids:
                try:
                    await application.bot.send_message(
                        chat_id=admin_id,
                        text="🛑 Bot telah dihentikan"
                    )
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Error dalam shutdown: {e}")
    
    # ==================== RUN BOT ====================
    
    print("🤖 Bot Telegram dengan fitur admin dan langganan sedang berjalan...")
    print("📱 Tekan Ctrl+C untuk menghentikan bot")
    print("👑 Admin panel: /admin")
    print("📊 Status user: /status")
    print("🛠️ Tools: /tools")
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n🛑 Bot dihentikan oleh pengguna")
        asyncio.run(shutdown_handler())
    except Exception as e:
        print(f"❌ Error: {e}")
        asyncio.run(shutdown_handler())

if __name__ == '__main__':
    main()