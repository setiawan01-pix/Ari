"""
Admin Handlers untuk Bot Telegram
Mengelola fitur-fitur admin seperti perpanjang langganan, notifikasi, dll
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime, timedelta
from typing import Dict, Any, List
from database import db_manager
from config import config

logger = logging.getLogger(__name__)

# States untuk conversation handler
WAITING_USER_ID, WAITING_DURATION = range(2)

class AdminManager:
    """Kelas untuk mengelola fitur admin"""
    
    def __init__(self):
        self.admin_ids = config.admin_ids
    
    def is_admin(self, user_id: int) -> bool:
        """Cek apakah user adalah admin"""
        return user_id in self.admin_ids
    
    async def admin_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Menu utama admin"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Anda tidak memiliki akses admin!")
            return
        
        keyboard = [
            [InlineKeyboardButton("🔁 Perpanjang Langganan", callback_data="admin_extend")],
            [InlineKeyboardButton("📊 Status Langganan", callback_data="admin_status")],
            [InlineKeyboardButton("👥 Daftar User", callback_data="admin_users")],
            [InlineKeyboardButton("📋 Log Admin", callback_data="admin_logs")],
            [InlineKeyboardButton("🔔 Test Notifikasi", callback_data="admin_notify")],
            [InlineKeyboardButton("❌ Tutup", callback_data="admin_close")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "👑 **ADMIN PANEL**\n\n"
            "Silakan pilih menu yang diinginkan:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def admin_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handler untuk callback admin"""
        query = update.callback_query
        await query.answer()
        
        if not self.is_admin(query.from_user.id):
            await query.edit_message_text("❌ Anda tidak memiliki akses admin!")
            return
        
        if query.data == "admin_extend":
            await self.start_extend_subscription(query, context)
        elif query.data == "admin_status":
            await self.show_subscription_status(query, context)
        elif query.data == "admin_users":
            await self.show_users_list(query, context)
        elif query.data == "admin_logs":
            await self.show_admin_logs(query, context)
        elif query.data == "admin_notify":
            await self.test_notification(query, context)
        elif query.data == "admin_close":
            await query.edit_message_text("✅ Admin panel ditutup")
    
    async def start_extend_subscription(self, query, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Mulai proses perpanjang langganan"""
        await query.edit_message_text(
            "🔁 **PERPANJANG LANGGANAN**\n\n"
            "Silakan ketik ID user yang akan diperpanjang langganannya.\n"
            "Atau reply ke pesan user tersebut.\n\n"
            "Contoh: `123456789`",
            parse_mode='Markdown'
        )
        context.user_data['admin_action'] = 'extend_subscription'
        return WAITING_USER_ID
    
    async def handle_user_id_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle input user ID untuk perpanjang langganan"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("❌ Anda tidak memiliki akses admin!")
            return ConversationHandler.END
        
        try:
            user_id = int(update.message.text)
            user = db_manager.get_user(user_id)
            
            if not user:
                await update.message.reply_text(
                    f"❌ User dengan ID `{user_id}` tidak ditemukan!\n"
                    "Silakan coba lagi atau ketik /cancel untuk membatalkan.",
                    parse_mode='Markdown'
                )
                return WAITING_USER_ID
            
            context.user_data['target_user_id'] = user_id
            context.user_data['target_user'] = user
            
            # Tampilkan pilihan durasi
            keyboard = [
                [InlineKeyboardButton("1 Hari", callback_data="duration_1")],
                [InlineKeyboardButton("7 Hari", callback_data="duration_7")],
                [InlineKeyboardButton("30 Hari", callback_data="duration_30")],
                [InlineKeyboardButton("90 Hari", callback_data="duration_90")],
                [InlineKeyboardButton("365 Hari", callback_data="duration_365")],
                [InlineKeyboardButton("❌ Batal", callback_data="admin_cancel")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"✅ User ditemukan!\n\n"
                f"👤 **Nama:** {user.get('first_name', 'N/A')}\n"
                f"🆔 **ID:** `{user_id}`\n"
                f"📅 **Status:** {user.get('subscription_status', 'free')}\n\n"
                f"Pilih durasi perpanjangan:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            return WAITING_DURATION
            
        except ValueError:
            await update.message.reply_text(
                "❌ ID user harus berupa angka!\n"
                "Contoh: `123456789`\n"
                "Atau ketik /cancel untuk membatalkan.",
                parse_mode='Markdown'
            )
            return WAITING_USER_ID
    
    async def handle_duration_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle pilihan durasi perpanjangan"""
        query = update.callback_query
        await query.answer()
        
        if not self.is_admin(query.from_user.id):
            await query.edit_message_text("❌ Anda tidak memiliki akses admin!")
            return ConversationHandler.END
        
        if query.data == "admin_cancel":
            await query.edit_message_text("❌ Perpanjangan langganan dibatalkan")
            return ConversationHandler.END
        
        try:
            duration = int(query.data.split('_')[1])
            user_id = context.user_data.get('target_user_id')
            user = context.user_data.get('target_user')
            
            if not user_id or not user:
                await query.edit_message_text("❌ Data user tidak ditemukan!")
                return ConversationHandler.END
            
            # Proses perpanjangan
            success = db_manager.update_user_subscription(
                user_id=user_id,
                subscription_type='premium',
                duration_days=duration,
                admin_id=query.from_user.id
            )
            
            if success:
                # Kirim notifikasi ke user
                try:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=f"🎉 **LANGGANAN DIPERPANJANG!**\n\n"
                             f"Selamat! Langganan Anda telah diperpanjang {duration} hari.\n"
                             f"📅 Berlaku hingga: {datetime.now() + timedelta(days=duration):%d/%m/%Y}\n\n"
                             f"Terima kasih telah menggunakan layanan kami! 🙏"
                    )
                except Exception as e:
                    logger.warning(f"Tidak bisa kirim notifikasi ke user {user_id}: {e}")
                
                await query.edit_message_text(
                    f"✅ **LANGGANAN BERHASIL DIPERPANJANG!**\n\n"
                    f"👤 **User:** {user.get('first_name', 'N/A')}\n"
                    f"🆔 **ID:** `{user_id}`\n"
                    f"⏰ **Durasi:** {duration} hari\n"
                    f"📅 **Berlaku hingga:** {datetime.now() + timedelta(days=duration):%d/%m/%Y}\n\n"
                    f"Notifikasi telah dikirim ke user.",
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text("❌ Gagal memperpanjang langganan!")
            
            return ConversationHandler.END
            
        except Exception as e:
            logger.error(f"Error dalam handle duration callback: {e}")
            await query.edit_message_text("❌ Terjadi kesalahan sistem!")
            return ConversationHandler.END
    
    async def show_subscription_status(self, query, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Tampilkan status langganan semua user"""
        users = db_manager.get_all_users(limit=50)
        
        if not users:
            await query.edit_message_text("📊 Tidak ada data user yang ditemukan.")
            return
        
        # Hitung statistik
        total_users = len(users)
        active_subscriptions = len([u for u in users if u['subscription_status'] != 'free'])
        expired_users = len([u for u in users if u['expired_date'] and datetime.fromisoformat(u['expired_date']) < datetime.now()])
        
        status_text = f"📊 **STATUS LANGGANAN**\n\n"
        status_text += f"👥 **Total User:** {total_users}\n"
        status_text += f"✅ **Langganan Aktif:** {active_subscriptions}\n"
        status_text += f"❌ **Langganan Habis:** {expired_users}\n\n"
        
        # Tampilkan user yang akan habis
        expiring_users = db_manager.get_expiring_subscriptions(days_threshold=7)
        if expiring_users:
            status_text += "⚠️ **Akan Habis (7 hari ke depan):**\n"
            for user in expiring_users[:5]:  # Tampilkan max 5
                expired_date = datetime.fromisoformat(user['expired_date'])
                days_left = (expired_date - datetime.now()).days
                status_text += f"• {user['first_name']} (ID: {user['user_id']}) - {days_left} hari lagi\n"
            status_text += "\n"
        
        # Tampilkan user yang sudah habis
        expired_users_list = db_manager.get_expired_subscriptions()
        if expired_users_list:
            status_text += "❌ **Sudah Habis:**\n"
            for user in expired_users_list[:5]:  # Tampilkan max 5
                expired_date = datetime.fromisoformat(user['expired_date'])
                days_expired = (datetime.now() - expired_date).days
                status_text += f"• {user['first_name']} (ID: {user['user_id']}) - {days_expired} hari yang lalu\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            status_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_users_list(self, query, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Tampilkan daftar user"""
        users = db_manager.get_all_users(limit=20)
        
        if not users:
            await query.edit_message_text("👥 Tidak ada data user yang ditemukan.")
            return
        
        users_text = "👥 **DAFTAR USER** (20 terbaru)\n\n"
        
        for i, user in enumerate(users, 1):
            status_emoji = "✅" if user['subscription_status'] != 'free' else "🆓"
            users_text += f"{i}. {status_emoji} {user['first_name']} (ID: `{user['user_id']}`)\n"
            users_text += f"   📅 Status: {user['subscription_status']}\n"
            if user['expired_date']:
                expired_date = datetime.fromisoformat(user['expired_date'])
                if expired_date < datetime.now():
                    users_text += f"   ❌ Habis: {expired_date:%d/%m/%Y}\n"
                else:
                    users_text += f"   ⏰ Expired: {expired_date:%d/%m/%Y}\n"
            users_text += "\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            users_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_admin_logs(self, query, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Tampilkan log aktivitas admin"""
        logs = db_manager.get_admin_actions(limit=10)
        
        if not logs:
            await query.edit_message_text("📋 Tidak ada log aktivitas admin.")
            return
        
        logs_text = "📋 **LOG AKTIVITAS ADMIN** (10 terbaru)\n\n"
        
        for log in logs:
            action_time = datetime.fromisoformat(log['created_at'])
            logs_text += f"🕐 {action_time:%d/%m/%Y %H:%M}\n"
            logs_text += f"👤 Admin ID: {log['admin_id']}\n"
            logs_text += f"📝 Aksi: {log['action_type']}\n"
            if log['target_user_id']:
                logs_text += f"🎯 Target: {log['target_user_id']}\n"
            logs_text += f"📄 Deskripsi: {log['description']}\n\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            logs_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def test_notification(self, query, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Test notifikasi ke admin"""
        try:
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text="🔔 **TEST NOTIFIKASI**\n\n"
                     "Ini adalah test notifikasi dari sistem bot.\n"
                     "Jika Anda menerima pesan ini, sistem notifikasi berfungsi dengan baik! ✅"
            )
            await query.edit_message_text("✅ Test notifikasi berhasil dikirim!")
        except Exception as e:
            logger.error(f"Error test notifikasi: {e}")
            await query.edit_message_text("❌ Gagal mengirim test notifikasi!")

# Instance global admin manager
admin_manager = AdminManager()