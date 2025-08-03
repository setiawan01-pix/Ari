#!/usr/bin/env python3
"""
Telegram Bot Script
A simple Telegram bot implementation using python-telegram-bot library
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token - ganti dengan token bot Anda
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk command /start"""
    user = update.effective_user
    welcome_message = f"""
🤖 Selamat datang di Bot Telegram!

Halo {user.first_name}! 👋

Saya adalah bot sederhana yang dapat membantu Anda.

📋 Perintah yang tersedia:
/start - Menampilkan pesan selamat datang ini
/help - Menampilkan bantuan
/info - Informasi tentang bot
/ping - Test koneksi bot

Silakan gunakan salah satu perintah di atas!
    """
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk command /help"""
    help_text = """
📚 Bantuan Bot Telegram

🔹 Perintah yang tersedia:
• /start - Pesan selamat datang
• /help - Menampilkan bantuan ini
• /info - Informasi bot
• /ping - Test koneksi

🔹 Fitur:
• Bot dapat merespon pesan teks
• Mendukung perintah dasar
• Logging untuk debugging

🔧 Cara menggunakan:
Ketik perintah yang diinginkan atau kirim pesan teks biasa.
    """
    await update.message.reply_text(help_text)

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
    
    # Respon sederhana berdasarkan pesan
    if user_message.lower() in ['halo', 'hello', 'hi', 'hai']:
        response = f"Halo {user.first_name}! 👋 Senang bertemu dengan Anda!"
    elif user_message.lower() in ['terima kasih', 'thanks', 'thank you']:
        response = "Sama-sama! 😊 Senang bisa membantu!"
    elif '?' in user_message:
        response = "Pertanyaan yang menarik! 🤔 Silakan gunakan /help untuk melihat perintah yang tersedia."
    else:
        response = f"Pesan Anda: '{user_message}'\n\nGunakan /help untuk melihat perintah yang tersedia."
    
    await update.message.reply_text(response)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk error"""
    logger.error(f"Exception while handling an update: {context.error}")
    if update and hasattr(update, 'message'):
        await update.message.reply_text("Maaf, terjadi kesalahan. Silakan coba lagi nanti.")

def main() -> None:
    """Fungsi utama untuk menjalankan bot"""
    # Cek token bot
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Error: Token bot belum diset!")
        print("🔧 Cara mengatur token:")
        print("1. Set environment variable: export BOT_TOKEN='your_token_here'")
        print("2. Atau edit langsung di file ini")
        return
    
    # Buat aplikasi bot
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Tambahkan handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("ping", ping_command))
    
    # Handler untuk pesan teks
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Jalankan bot
    print("🤖 Bot Telegram sedang berjalan...")
    print("📱 Tekan Ctrl+C untuk menghentikan bot")
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n🛑 Bot dihentikan oleh pengguna")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()