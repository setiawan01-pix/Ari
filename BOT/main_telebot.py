#!/usr/bin/env python3
"""
Bot Konversi Kontak Telegram - Versi pyTelegramBotAPI
Kompatibel dengan Python 3.13
"""

import logging
import os
import json
from datetime import datetime, timedelta
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from functools import wraps

# Konfigurasi
TOKEN = "8198867479:AAEtUhyTID-crNvg8fohpfvTYkYtIEDz6aQ"
ADMIN_ID = 8141075788
TRIAL_DURATION_HOURS = 1

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Data storage
USER_DATA_FILE = "user_data.json"
CUSTOMIZATION_FILE = "customization.json"
LOG_FILE = "log.txt"

# Create bot instance
bot = telebot.TeleBot(TOKEN)

def admin_only(func):
    @wraps(func)
    def wrapped(message, *args, **kwargs):
        user_id = message.from_user.id
        if user_id != ADMIN_ID:
            bot.reply_to(message, "❌ Anda tidak memiliki izin untuk menggunakan perintah ini.")
            return
        return func(message, *args, **kwargs)
    return wrapped

def load_user_data():
    """Load user data from JSON file"""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_user_data(data):
    """Save user data to JSON file"""
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_customization():
    """Load customization data"""
    if os.path.exists(CUSTOMIZATION_FILE):
        with open(CUSTOMIZATION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "welcome_message": "🔐 SISTEM AKSES USER\n\n🧪 Trial 1 Jam\n🔐 Premium (Berbayar)\nℹ️ Info Bot\n\nTrial: aktif 1jam → auto expired\nPremium: tampilkan harga + QR → admin aktifkan",
        "payment_method": "Transfer Bank",
        "prices": {
            "1_hari": 5000,
            "7_hari": 25000,
            "30_hari": 75000,
            "lifetime": 200000
        }
    }

def save_customization(data):
    """Save customization data"""
    with open(CUSTOMIZATION_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def log_activity(user_id, action):
    """Log user activity"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} ID:{user_id} ➝ {action}\n"
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def check_user_access(user_id):
    """Check if user has access"""
    user_data = load_user_data()
    user_id_str = str(user_id)
    
    if user_id_str not in user_data:
        return {"has_access": False, "reason": "User not registered"}
    
    user = user_data[user_id_str]
    now = datetime.now()
    
    # Check trial
    if user.get("status") == "trial" and user.get("trial_end"):
        trial_end = datetime.fromisoformat(user["trial_end"])
        if now < trial_end:
            return {"has_access": True, "status": "trial", "expires": trial_end}
        else:
            user["status"] = "expired"
            save_user_data(user_data)
            return {"has_access": False, "reason": "Trial expired"}
    
    # Check premium
    if user.get("status") == "premium":
        if user.get("premium_plan") == "lifetime":
            return {"has_access": True, "status": "premium", "plan": "lifetime"}
        
        if user.get("premium_end"):
            premium_end = datetime.fromisoformat(user["premium_end"])
            if now < premium_end:
                return {"has_access": True, "status": "premium", "expires": premium_end}
            else:
                user["status"] = "expired"
                save_user_data(user_data)
                return {"has_access": False, "reason": "Premium expired"}
    
    return {"has_access": False, "reason": "No active subscription"}

def activate_trial(user_id):
    """Activate trial for user"""
    user_data = load_user_data()
    user_id_str = str(user_id)
    
    if user_id_str not in user_data:
        user_data[user_id_str] = {
            "user_id": user_id,
            "status": "inactive",
            "created_at": datetime.now().isoformat()
        }
    
    user = user_data[user_id_str]
    
    # Check if user already had trial
    if user.get("trial_start"):
        return False
    
    now = datetime.now()
    trial_end = now + timedelta(hours=TRIAL_DURATION_HOURS)
    
    user["status"] = "trial"
    user["trial_start"] = now.isoformat()
    user["trial_end"] = trial_end.isoformat()
    
    save_user_data(user_data)
    return True

def activate_premium(user_id, plan, days=None):
    """Activate premium for user"""
    user_data = load_user_data()
    user_id_str = str(user_id)
    
    if user_id_str not in user_data:
        user_data[user_id_str] = {
            "user_id": user_id,
            "status": "inactive",
            "created_at": datetime.now().isoformat()
        }
    
    user = user_data[user_id_str]
    now = datetime.now()
    
    if plan == "lifetime":
        premium_end = None
    else:
        premium_end = now + timedelta(days=days)
    
    user["status"] = "premium"
    user["premium_start"] = now.isoformat()
    user["premium_end"] = premium_end.isoformat() if premium_end else None
    user["premium_plan"] = plan
    
    save_user_data(user_data)
    return True

# Menu functions
def main_menu():
    """Main menu"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("🧪 Trial 1 Jam", callback_data='trial'))
    keyboard.row(InlineKeyboardButton("🔐 Premium (Berbayar)", callback_data='premium'))
    keyboard.row(InlineKeyboardButton("ℹ️ Info Bot", callback_data='info'))
    return keyboard

def main_menu_admin():
    """Main menu for admin"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("🧪 Trial 1 Jam", callback_data='trial'))
    keyboard.row(InlineKeyboardButton("🔐 Premium (Berbayar)", callback_data='premium'))
    keyboard.row(InlineKeyboardButton("ℹ️ Info Bot", callback_data='info'))
    keyboard.row(InlineKeyboardButton("👑 Admin Panel", callback_data='admin_panel'))
    return keyboard

def features_menu():
    """Features menu"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("📁 Fitur Konversi", callback_data='conversion_features'))
    keyboard.row(InlineKeyboardButton("🛠️ File Tools", callback_data='file_tools'))
    keyboard.row(InlineKeyboardButton("🧾 Input Manual", callback_data='manual_input'))
    keyboard.row(InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main'))
    return keyboard

def conversion_menu():
    """Conversion menu"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("📂 TXT ➝ VCF (Format TUTOR KIKS)", callback_data='conv_txt_to_vcf'))
    keyboard.row(InlineKeyboardButton("✂️ TXT ➝ TXT (Split)", callback_data='conv_split_txt'))
    keyboard.row(InlineKeyboardButton("📤 VCF ➝ TXT", callback_data='conv_vcf_to_txt'))
    keyboard.row(InlineKeyboardButton("📊 XLS ➝ VCF", callback_data='conv_xls_to_vcf'))
    keyboard.row(InlineKeyboardButton("🔙 Kembali", callback_data='back_to_features'))
    return keyboard

def file_tools_menu():
    """File tools menu"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("📎 Gabungkan File", callback_data='merge_files'))
    keyboard.row(InlineKeyboardButton("🔍 Cek Duplikat", callback_data='check_duplicates'))
    keyboard.row(InlineKeyboardButton("➕ Tambah Kontak", callback_data='add_contact'))
    keyboard.row(InlineKeyboardButton("✏️ Rename File", callback_data='rename_file'))
    keyboard.row(InlineKeyboardButton("❌ Hapus Nomor", callback_data='delete_number'))
    keyboard.row(InlineKeyboardButton("✂️ Pecah File", callback_data='split_file_tool'))
    keyboard.row(InlineKeyboardButton("🔙 Kembali", callback_data='back_to_features'))
    return keyboard

def premium_menu():
    """Premium menu"""
    custom_data = load_customization()
    prices = custom_data.get("prices", {})
    
    keyboard = InlineKeyboardMarkup()
    for plan, price in prices.items():
        plan_name = plan.replace("_", " ").title()
        keyboard.row(InlineKeyboardButton(f"{plan_name} - Rp {price:,}", callback_data=f'premium_{plan}'))
    
    keyboard.row(InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main'))
    return keyboard

def admin_menu():
    """Admin menu"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("📢 Broadcast", callback_data='admin_broadcast'))
    keyboard.row(InlineKeyboardButton("💳 Ganti QR / Metode Bayar", callback_data='admin_payment'))
    keyboard.row(InlineKeyboardButton("🛠️ Atur Harga Premium", callback_data='admin_prices'))
    keyboard.row(InlineKeyboardButton("👥 Lihat Daftar User", callback_data='admin_users'))
    keyboard.row(InlineKeyboardButton("➕ Tambah User Manual", callback_data='admin_adduser'))
    keyboard.row(InlineKeyboardButton("❌ Kick User", callback_data='admin_kick'))
    keyboard.row(InlineKeyboardButton("🖊️ Ubah Teks Sambutan", callback_data='admin_welcome'))
    keyboard.row(InlineKeyboardButton("📋 Log Aktivitas", callback_data='admin_logs'))
    keyboard.row(InlineKeyboardButton("🔙 Kembali", callback_data='back_to_main'))
    return keyboard

def cancel_button():
    """Cancel button"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("❌ Batal", callback_data='cancel'))
    return keyboard

def back_button(callback_data):
    """Back button"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("🔙 Kembali", callback_data=callback_data))
    return keyboard

# Command handlers
@bot.message_handler(commands=['start'])
def start(message):
    """Handle /start command"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    log_activity(user_id, "/start")
    
    # Check if user is admin
    is_admin = (user_id == ADMIN_ID)
    
    # Check access
    access_info = check_user_access(user_id)
    
    if access_info["has_access"]:
        custom_data = load_customization()
        welcome_message = custom_data.get("welcome_message", "Selamat datang!")
        
        bot.reply_to(
            message,
            f"✅ Selamat datang kembali!\n\n"
            f"Status: {access_info['status']}\n"
            f"Silakan pilih fitur yang ingin digunakan:",
            reply_markup=features_menu()
        )
    else:
        custom_data = load_customization()
        welcome_message = custom_data.get("welcome_message", "Selamat datang!")
        
        # Show admin menu if user is admin
        if is_admin:
            bot.reply_to(message, welcome_message, reply_markup=main_menu_admin())
        else:
            bot.reply_to(message, welcome_message, reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def button_handler(call):
    """Handle button callbacks"""
    user_id = call.from_user.id
    callback_data = call.data
    
    log_activity(user_id, f"Button: {callback_data}")
    
    if callback_data == 'trial':
        handle_trial(call)
    elif callback_data == 'premium':
        handle_premium(call)
    elif callback_data == 'info':
        handle_info(call)
    elif callback_data == 'admin_panel':
        handle_admin_panel(call)
    elif callback_data == 'conversion_features':
        handle_conversion_features(call)
    elif callback_data == 'file_tools':
        handle_file_tools(call)
    elif callback_data == 'manual_input':
        handle_manual_input(call)
    elif callback_data.startswith('conv_'):
        handle_conversion_option(call)
    elif callback_data.startswith('premium_'):
        handle_premium_selection(call)
    elif callback_data.startswith('admin_'):
        handle_admin_option(call)
    elif callback_data == 'cancel':
        handle_cancel(call)
    elif callback_data.startswith('back_'):
        handle_back(call)
    else:
        handle_file_tools_callback(call)

def handle_trial(call):
    """Handle trial activation"""
    user_id = call.from_user.id
    
    access_info = check_user_access(user_id)
    if access_info["has_access"]:
        bot.edit_message_text(
            "✅ Anda sudah memiliki akses aktif!\n\n"
            f"Status: {access_info['status']}\n"
            "Silakan gunakan fitur-fitur bot.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=features_menu()
        )
        return
    
    success = activate_trial(user_id)
    if success:
        bot.edit_message_text(
            "🧪 Trial berhasil diaktifkan!\n\n"
            "⏰ Durasi: 1 jam\n"
            "✅ Akses ke semua fitur\n\n"
            "Silakan pilih fitur yang ingin digunakan:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=features_menu()
        )
    else:
        bot.edit_message_text(
            "❌ Trial sudah pernah digunakan!\n\n"
            "Silakan pilih opsi Premium untuk akses penuh.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=main_menu()
        )

def handle_premium(call):
    """Handle premium menu"""
    custom_data = load_customization()
    
    message = "🔐 PREMIUM SUBSCRIPTION\n\n"
    message += "Pilih paket yang sesuai:\n\n"
    
    prices = custom_data.get("prices", {})
    for plan, price in prices.items():
        plan_name = plan.replace("_", " ").title()
        message += f"• {plan_name}: Rp {price:,}\n"
    
    message += "\n💳 Metode Pembayaran:\n"
    message += f"• {custom_data.get('payment_method', 'Transfer Bank')}\n\n"
    message += "Silakan pilih paket:"
    
    bot.edit_message_text(
        message,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=premium_menu()
    )

def handle_premium_selection(call):
    """Handle premium plan selection"""
    plan = call.data.replace('premium_', '')
    
    custom_data = load_customization()
    prices = custom_data.get("prices", {})
    price = prices.get(plan, 0)
    
    message = f"🔐 PREMIUM {plan.replace('_', ' ').upper()}\n\n"
    message += f"💰 Harga: Rp {price:,}\n"
    message += f"💳 Metode: {custom_data.get('payment_method', 'Transfer Bank')}\n\n"
    message += "📞 Hubungi admin untuk informasi pembayaran.\n\n"
    message += "Admin ID: " + str(ADMIN_ID)
    
    bot.edit_message_text(
        message,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=back_button('premium')
    )

def handle_info(call):
    """Handle info bot"""
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
    
    bot.edit_message_text(
        message,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=back_button('back_to_main')
    )

def handle_admin_panel(call):
    """Handle admin panel"""
    user_id = call.from_user.id
    
    if user_id != ADMIN_ID:
        bot.edit_message_text(
            "❌ Anda tidak memiliki izin untuk mengakses panel admin!",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_button('back_to_main')
        )
        return
    
    bot.edit_message_text(
        "👑 ADMIN PANEL\n\n"
        "Pilih fitur admin yang ingin digunakan:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=admin_menu()
    )

def handle_conversion_features(call):
    """Handle conversion features menu"""
    user_id = call.from_user.id
    
    access_info = check_user_access(user_id)
    if not access_info["has_access"]:
        bot.edit_message_text(
            "❌ Akses ditolak!\n\n"
            f"Alasan: {access_info['reason']}\n\n"
            "Silakan pilih Trial atau Premium untuk mengakses fitur.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=main_menu()
        )
        return
    
    bot.edit_message_text(
        "📁 FITUR KONVERSI\n\n"
        "Pilih jenis konversi yang diinginkan:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=conversion_menu()
    )

def handle_file_tools(call):
    """Handle file tools menu"""
    user_id = call.from_user.id
    
    access_info = check_user_access(user_id)
    if not access_info["has_access"]:
        bot.edit_message_text(
            "❌ Akses ditolak!\n\n"
            f"Alasan: {access_info['reason']}\n\n"
            "Silakan pilih Trial atau Premium untuk mengakses fitur.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=main_menu()
        )
        return
    
    bot.edit_message_text(
        "🛠️ FILE TOOLS\n\n"
        "Pilih tool yang ingin digunakan:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=file_tools_menu()
    )

def handle_manual_input(call):
    """Handle manual input menu"""
    user_id = call.from_user.id
    
    access_info = check_user_access(user_id)
    if not access_info["has_access"]:
        bot.edit_message_text(
            "❌ Akses ditolak!\n\n"
            f"Alasan: {access_info['reason']}\n\n"
            "Silakan pilih Trial atau Premium untuk mengakses fitur.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=main_menu()
        )
        return
    
    bot.edit_message_text(
        "🧾 INPUT MANUAL\n\n"
        "Fitur input manual akan segera hadir.\n"
        "Silakan pilih fitur lain terlebih dahulu.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=back_button('back_to_features')
    )

def handle_conversion_option(call):
    """Handle conversion option selection"""
    conversion_type = call.data.replace('conv_', '')
    
    user_id = call.from_user.id
    access_info = check_user_access(user_id)
    if not access_info["has_access"]:
        bot.edit_message_text(
            "❌ Akses ditolak!\n\n"
            f"Alasan: {access_info['reason']}\n\n"
            "Silakan pilih Trial atau Premium untuk mengakses fitur.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=main_menu()
        )
        return
    
    if conversion_type == 'txt_to_vcf':
        bot.edit_message_text(
            "📂 TXT ➝ VCF (Format TUTOR KIKS)\n\n"
            "Silakan kirim file .txt yang berisi nomor telepon (satu nomor per baris).\n\n"
            "Setelah file diterima, bot akan meminta:\n"
            "• Nama file dasar\n"
            "• Nama kontak dasar\n"
            "• Jumlah kontak per file\n"
            "• Urutan awal file",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=cancel_button()
        )
    elif conversion_type == 'split_txt':
        bot.edit_message_text(
            "✂️ TXT ➝ TXT (Split)\n\n"
            "Silakan kirim file .txt yang ingin dibagi.\n\n"
            "Bot akan meminta jumlah baris per file.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=cancel_button()
        )
    elif conversion_type == 'vcf_to_txt':
        bot.edit_message_text(
            "📤 VCF ➝ TXT\n\n"
            "Silakan kirim file .vcf yang ingin diekstrak nomornya.\n\n"
            "Bot akan mengekstrak semua nomor telepon dan menyimpannya dalam file .txt.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=cancel_button()
        )
    elif conversion_type == 'xls_to_vcf':
        bot.edit_message_text(
            "📊 XLS ➝ VCF\n\n"
            "Silakan kirim file .xls atau .xlsx.\n\n"
            "Bot akan membaca:\n"
            "• Kolom A = Nama\n"
            "• Kolom B = Nomor\n\n"
            "Dan mengkonversi ke format VCF.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=cancel_button()
        )

def handle_admin_option(call):
    """Handle admin options"""
    user_id = call.from_user.id
    
    if user_id != ADMIN_ID:
        bot.edit_message_text(
            "❌ Anda tidak memiliki izin untuk mengakses menu admin!",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_button('back_to_main')
        )
        return
    
    admin_option = call.data.replace('admin_', '')
    
    if admin_option == 'broadcast':
        bot.edit_message_text(
            "📢 BROADCAST MESSAGE\n\n"
            "Silakan ketik pesan yang ingin disiarkan ke semua user:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=cancel_button()
        )
    elif admin_option == 'payment':
        bot.edit_message_text(
            "💳 GANTI METODE PEMBAYARAN\n\n"
            "Silakan kirim QR code atau ketik metode pembayaran baru:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=cancel_button()
        )
    elif admin_option == 'prices':
        bot.edit_message_text(
            "🛠️ ATUR HARGA PREMIUM\n\n"
            "Silakan ketik harga dalam format:\n"
            "1_hari:5000\n"
            "7_hari:25000\n"
            "30_hari:75000\n"
            "lifetime:200000",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=cancel_button()
        )
    elif admin_option == 'users':
        handle_admin_users(call)
    elif admin_option == 'logs':
        handle_admin_logs(call)
    else:
        bot.edit_message_text(
            "🛠️ ADMIN PANEL\n\n"
            "Fitur sedang dalam pengembangan.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=admin_menu()
        )

def handle_admin_users(call):
    """Handle admin users list"""
    user_data = load_user_data()
    users = []
    
    for user_id, user in user_data.items():
        access_info = check_user_access(int(user_id))
        user_info = {
            "user_id": user_id,
            "username": user.get("username"),
            "status": user.get("status"),
            "has_access": access_info["has_access"],
            "created_at": user.get("created_at")
        }
        
        if access_info.get("expires"):
            user_info["expires"] = access_info["expires"].isoformat()
        
        users.append(user_info)
    
    # Calculate stats
    total = len(users)
    trial = sum(1 for user in users if user['status'] == 'trial')
    premium = sum(1 for user in users if user['status'] == 'premium')
    expired = sum(1 for user in users if user['status'] == 'expired')
    
    message = "👥 DAFTAR USER\n\n"
    message += f"📊 Statistik:\n"
    message += f"• Total: {total}\n"
    message += f"• Trial: {trial}\n"
    message += f"• Premium: {premium}\n"
    message += f"• Expired: {expired}\n\n"
    
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
    
    bot.edit_message_text(
        message,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=admin_menu()
    )

def handle_admin_logs(call):
    """Handle admin logs"""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
        
        recent_lines = all_lines[-20:] if len(all_lines) > 20 else all_lines
        logs = ''.join(recent_lines)
        
        if logs:
            message = "📋 LOG AKTIVITAS (20 terakhir)\n\n"
            message += logs
        else:
            message = "📋 LOG AKTIVITAS\n\nBelum ada aktivitas yang tercatat."
    else:
        message = "📋 LOG AKTIVITAS\n\nLog file tidak ditemukan."
    
    bot.edit_message_text(
        message,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=admin_menu()
    )

def handle_file_tools_callback(call):
    """Handle file tools callbacks"""
    callback_data = call.data
    
    user_id = call.from_user.id
    access_info = check_user_access(user_id)
    if not access_info["has_access"]:
        bot.edit_message_text(
            "❌ Akses ditolak!\n\n"
            f"Alasan: {access_info['reason']}\n\n"
            "Silakan pilih Trial atau Premium untuk mengakses fitur.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=main_menu()
        )
        return
    
    bot.edit_message_text(
        "🛠️ FILE TOOLS\n\n"
        "Fitur file tools akan segera hadir.\n"
        "Silakan pilih fitur lain terlebih dahulu.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=back_button('back_to_file_tools')
    )

def handle_cancel(call):
    """Handle cancel button"""
    bot.edit_message_text(
        "❌ Operasi dibatalkan.\n\n"
        "Silakan pilih menu lain:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=main_menu()
    )

def handle_back(call):
    """Handle back button"""
    callback_data = call.data
    
    if callback_data == 'back_to_main':
        user_id = call.from_user.id
        is_admin = (user_id == ADMIN_ID)
        
        if is_admin:
            bot.edit_message_text(
                "🔐 SISTEM AKSES USER\n\n"
                "Silakan pilih opsi:",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=main_menu_admin()
            )
        else:
            bot.edit_message_text(
                "🔐 SISTEM AKSES USER\n\n"
                "Silakan pilih opsi:",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=main_menu()
            )
    elif callback_data == 'back_to_features':
        bot.edit_message_text(
            "📁 FITUR UTAMA\n\n"
            "Silakan pilih kategori fitur:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=features_menu()
        )
    elif callback_data == 'back_to_file_tools':
        bot.edit_message_text(
            "🛠️ FILE TOOLS\n\n"
            "Pilih tool yang ingin digunakan:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=file_tools_menu()
        )
    elif callback_data == 'premium':
        handle_premium(call)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    """Handle file upload"""
    user_id = message.from_user.id
    
    access_info = check_user_access(user_id)
    if not access_info["has_access"]:
        bot.reply_to(
            message,
            "❌ Akses ditolak!\n\n"
            f"Alasan: {access_info['reason']}\n\n"
            "Silakan pilih Trial atau Premium untuk mengakses fitur.",
            reply_markup=back_button('back_to_main')
        )
        return
    
    bot.reply_to(
        message,
        "📁 File diterima!\n\n"
        "Fitur konversi file akan segera hadir.\n"
        "Silakan pilih fitur lain terlebih dahulu.",
        reply_markup=back_button('back_to_features')
    )

# Admin commands
@bot.message_handler(commands=['adduser'])
@admin_only
def adduser(message):
    """Add user manually"""
    try:
        args = message.text.split()[1:]
        if len(args) != 2:
            bot.reply_to(message, "Format: /adduser <user_id> <days>")
            return
        
        user_id = int(args[0])
        days = int(args[1])
        
        success = activate_premium(user_id, "custom", days)
        if success:
            bot.reply_to(message, f"✅ User {user_id} berhasil ditambahkan untuk {days} hari.")
        else:
            bot.reply_to(message, f"❌ Gagal menambahkan user {user_id}.")
    except (ValueError, IndexError):
        bot.reply_to(message, "❌ Format tidak valid. Gunakan: /adduser <user_id> <days>")

@bot.message_handler(commands=['kick'])
@admin_only
def kick(message):
    """Kick user"""
    try:
        args = message.text.split()[1:]
        if len(args) != 1:
            bot.reply_to(message, "Format: /kick <user_id>")
            return
        
        user_id = int(args[0])
        user_data = load_user_data()
        user_id_str = str(user_id)
        
        if user_id_str in user_data:
            del user_data[user_id_str]
            save_user_data(user_data)
            bot.reply_to(message, f"✅ User {user_id} berhasil dihapus.")
        else:
            bot.reply_to(message, f"❌ User {user_id} tidak ditemukan.")
    except (ValueError, IndexError):
        bot.reply_to(message, "❌ Format tidak valid. Gunakan: /kick <user_id>")

@bot.message_handler(commands=['ubahsambutan'])
@admin_only
def ubahsambutan(message):
    """Change welcome message"""
    try:
        args = message.text.split()[1:]
        if not args:
            bot.reply_to(message, "Format: /ubahsambutan <pesan baru>")
            return
        
        new_message = " ".join(args)
        custom_data = load_customization()
        custom_data["welcome_message"] = new_message
        save_customization(custom_data)
        
        bot.reply_to(message, "✅ Pesan sambutan berhasil diubah!")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

def main():
    """Start the bot"""
    print("🤖 Bot starting...")
    print(f"📱 Token: {TOKEN}")
    print(f"👑 Admin ID: {ADMIN_ID}")
    print("✅ Bot is running!")
    
    # Start polling
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()