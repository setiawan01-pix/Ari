"""
Sistem Notifikasi untuk Bot Telegram
Mengelola notifikasi otomatis untuk langganan yang akan habis atau sudah habis
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
from telegram import Bot
from database import db_manager
from config import config

logger = logging.getLogger(__name__)

class NotificationSystem:
    """Kelas untuk mengelola sistem notifikasi"""
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self.is_running = False
        self.notification_task = None
    
    async def start_notification_service(self):
        """Mulai layanan notifikasi otomatis"""
        if self.is_running:
            logger.warning("Layanan notifikasi sudah berjalan")
            return
        
        self.is_running = True
        logger.info("🚀 Layanan notifikasi otomatis dimulai")
        
        # Jalankan task notifikasi
        self.notification_task = asyncio.create_task(self._notification_loop())
    
    async def stop_notification_service(self):
        """Hentikan layanan notifikasi"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.notification_task:
            self.notification_task.cancel()
            try:
                await self.notification_task
            except asyncio.CancelledError:
                pass
        
        logger.info("🛑 Layanan notifikasi dihentikan")
    
    async def _notification_loop(self):
        """Loop utama untuk notifikasi"""
        while self.is_running:
            try:
                await self._check_and_send_notifications()
                # Tunggu 1 jam sebelum cek lagi
                await asyncio.sleep(3600)  # 1 jam
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error dalam notification loop: {e}")
                await asyncio.sleep(300)  # Tunggu 5 menit jika error
    
    async def _check_and_send_notifications(self):
        """Cek dan kirim notifikasi yang diperlukan"""
        logger.info("🔍 Mengecek notifikasi yang perlu dikirim...")
        
        # Cek user yang langganannya akan habis dalam 1 hari
        await self._send_expiring_notifications(days_threshold=1)
        
        # Cek user yang langganannya sudah habis
        await self._send_expired_notifications()
        
        # Cek user yang langganannya akan habis dalam 7 hari
        await self._send_expiring_notifications(days_threshold=7)
    
    async def _send_expiring_notifications(self, days_threshold: int):
        """Kirim notifikasi untuk langganan yang akan habis"""
        expiring_users = db_manager.get_expiring_subscriptions(days_threshold=days_threshold)
        
        for user in expiring_users:
            try:
                # Cek apakah notifikasi sudah dikirim hari ini
                if await self._should_send_notification(user['user_id'], f"expiring_{days_threshold}"):
                    await self._send_expiring_message(user, days_threshold)
                    await asyncio.sleep(1)  # Delay untuk menghindari rate limit
            except Exception as e:
                logger.error(f"Error kirim notifikasi expiring ke user {user['user_id']}: {e}")
    
    async def _send_expired_notifications(self):
        """Kirim notifikasi untuk langganan yang sudah habis"""
        expired_users = db_manager.get_expired_subscriptions()
        
        for user in expired_users:
            try:
                # Cek apakah notifikasi sudah dikirim hari ini
                if await self._should_send_notification(user['user_id'], "expired"):
                    await self._send_expired_message(user)
                    await asyncio.sleep(1)  # Delay untuk menghindari rate limit
            except Exception as e:
                logger.error(f"Error kirim notifikasi expired ke user {user['user_id']}: {e}")
    
    async def _should_send_notification(self, user_id: int, notification_type: str) -> bool:
        """Cek apakah notifikasi sudah dikirim hari ini"""
        try:
            # Cek log notifikasi hari ini
            today = datetime.now().date()
            
            # Ambil notifikasi terakhir untuk user ini
            with db_manager.db_path as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT sent_at FROM notifications 
                    WHERE user_id = ? AND notification_type = ?
                    ORDER BY sent_at DESC LIMIT 1
                ''', (user_id, notification_type))
                
                row = cursor.fetchone()
                if row:
                    last_sent = datetime.fromisoformat(row[0]).date()
                    return last_sent < today
            
            return True
        except Exception as e:
            logger.error(f"Error cek notifikasi history: {e}")
            return True
    
    async def _send_expiring_message(self, user: Dict[str, Any], days_left: int):
        """Kirim pesan notifikasi langganan akan habis"""
        try:
            expired_date = datetime.fromisoformat(user['expired_date'])
            
            if days_left == 1:
                message = (
                    "⏳ **PERINGATAN LANGGANAN**\n\n"
                    f"Halo {user['first_name']}! 👋\n\n"
                    "⚠️ Langganan Anda akan **HABIS BESOK**!\n"
                    f"📅 Tanggal expired: {expired_date:%d/%m/%Y}\n\n"
                    "🔁 Untuk memperpanjang langganan, silakan hubungi admin.\n"
                    "💬 Gunakan command /contact untuk menghubungi admin.\n\n"
                    "Terima kasih telah menggunakan layanan kami! 🙏"
                )
            else:
                message = (
                    "⚠️ **PERINGATAN LANGGANAN**\n\n"
                    f"Halo {user['first_name']}! 👋\n\n"
                    f"📅 Langganan Anda akan habis dalam **{days_left} hari**.\n"
                    f"📅 Tanggal expired: {expired_date:%d/%m/%Y}\n\n"
                    "🔁 Untuk memperpanjang langganan, silakan hubungi admin.\n"
                    "💬 Gunakan command /contact untuk menghubungi admin.\n\n"
                    "Terima kasih telah menggunakan layanan kami! 🙏"
                )
            
            await self.bot.send_message(
                chat_id=user['user_id'],
                text=message,
                parse_mode='Markdown'
            )
            
            # Log notifikasi
            db_manager.add_notification_log(
                user_id=user['user_id'],
                notification_type=f"expiring_{days_left}",
                message=f"Notifikasi langganan akan habis dalam {days_left} hari"
            )
            
            logger.info(f"✅ Notifikasi expiring {days_left} hari dikirim ke user {user['user_id']}")
            
        except Exception as e:
            logger.error(f"Error kirim pesan expiring ke user {user['user_id']}: {e}")
    
    async def _send_expired_message(self, user: Dict[str, Any]):
        """Kirim pesan notifikasi langganan sudah habis"""
        try:
            expired_date = datetime.fromisoformat(user['expired_date'])
            days_expired = (datetime.now() - expired_date).days
            
            message = (
                "❌ **LANGGANAN HABIS**\n\n"
                f"Halo {user['first_name']}! 👋\n\n"
                "❌ Langganan Anda **SUDAH HABIS**!\n"
                f"📅 Tanggal expired: {expired_date:%d/%m/%Y}\n"
                f"⏰ Habis {days_expired} hari yang lalu\n\n"
                "🔒 Akses fitur premium telah dibatasi.\n"
                "🔁 Untuk mengaktifkan kembali, silakan perpanjang langganan.\n"
                "💬 Hubungi admin dengan command /contact\n\n"
                "Terima kasih telah menggunakan layanan kami! 🙏"
            )
            
            await self.bot.send_message(
                chat_id=user['user_id'],
                text=message,
                parse_mode='Markdown'
            )
            
            # Log notifikasi
            db_manager.add_notification_log(
                user_id=user['user_id'],
                notification_type="expired",
                message="Notifikasi langganan sudah habis"
            )
            
            logger.info(f"✅ Notifikasi expired dikirim ke user {user['user_id']}")
            
        except Exception as e:
            logger.error(f"Error kirim pesan expired ke user {user['user_id']}: {e}")
    
    async def send_custom_notification(self, user_id: int, message: str, notification_type: str = "custom"):
        """Kirim notifikasi kustom ke user tertentu"""
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
            
            # Log notifikasi
            db_manager.add_notification_log(
                user_id=user_id,
                notification_type=notification_type,
                message="Notifikasi kustom dari admin"
            )
            
            logger.info(f"✅ Notifikasi kustom dikirim ke user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error kirim notifikasi kustom ke user {user_id}: {e}")
            return False
    
    async def send_bulk_notification(self, user_ids: List[int], message: str, notification_type: str = "bulk"):
        """Kirim notifikasi massal ke banyak user"""
        success_count = 0
        failed_count = 0
        
        for user_id in user_ids:
            try:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode='Markdown'
                )
                
                # Log notifikasi
                db_manager.add_notification_log(
                    user_id=user_id,
                    notification_type=notification_type,
                    message="Notifikasi massal dari admin"
                )
                
                success_count += 1
                await asyncio.sleep(0.5)  # Delay untuk menghindari rate limit
                
            except Exception as e:
                logger.error(f"Error kirim notifikasi massal ke user {user_id}: {e}")
                failed_count += 1
        
        logger.info(f"📢 Notifikasi massal selesai: {success_count} berhasil, {failed_count} gagal")
        return {"success": success_count, "failed": failed_count}
    
    async def send_admin_notification(self, admin_id: int, message: str):
        """Kirim notifikasi ke admin"""
        try:
            await self.bot.send_message(
                chat_id=admin_id,
                text=f"👑 **ADMIN NOTIFICATION**\n\n{message}",
                parse_mode='Markdown'
            )
            return True
        except Exception as e:
            logger.error(f"Error kirim notifikasi ke admin {admin_id}: {e}")
            return False

# Instance global notification system (akan diinisialisasi di main bot)
notification_system = None