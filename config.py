"""
Konfigurasi Bot Telegram
File ini berisi pengaturan konfigurasi untuk bot
"""

import os
from typing import Optional

class BotConfig:
    """Kelas konfigurasi bot"""
    
    def __init__(self):
        # Token bot - ambil dari environment variable atau set default
        self.token: str = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
        
        # Nama bot
        self.bot_name: str = "Telegram Bot Python"
        
        # Username bot (opsional)
        self.bot_username: Optional[str] = None
        
        # Pengaturan logging
        self.log_level: str = "INFO"
        self.log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Pengaturan polling
        self.polling_timeout: int = 30
        self.polling_read_timeout: int = 30
        
        # Pengaturan rate limiting
        self.rate_limit: float = 0.1  # detik antara request
        
        # Pengaturan webhook (untuk production)
        self.webhook_url: Optional[str] = None
        self.webhook_port: int = 8443
        
        # Pengaturan admin
        self.admin_ids: list = [123456789]  # List ID admin Telegram - Ganti dengan ID admin Anda
        
        # Pengaturan fitur
        self.enable_echo: bool = True
        self.enable_logging: bool = True
        self.enable_error_handling: bool = True
        
        # Pesan default
        self.welcome_message: str = """
🤖 Selamat datang di Bot Telegram!

Saya adalah bot sederhana yang dapat membantu Anda.

📋 Perintah yang tersedia:
/start - Menampilkan pesan selamat datang ini
/help - Menampilkan bantuan
/info - Informasi tentang bot
/ping - Test koneksi bot

Silakan gunakan salah satu perintah di atas!
        """
        
        self.help_message: str = """
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
        
        self.info_message: str = """
ℹ️ Informasi Bot

🤖 Nama: {bot_name}
📅 Dibuat dengan: python-telegram-bot
🐍 Bahasa: Python 3
📊 Status: Aktif

💡 Bot ini dibuat sebagai contoh implementasi dasar bot Telegram menggunakan Python.
        """
    
    def is_token_set(self) -> bool:
        """Cek apakah token bot sudah diset"""
        return self.token != 'YOUR_BOT_TOKEN_HERE' and self.token.strip() != ''
    
    def get_info_message(self) -> str:
        """Dapatkan pesan info dengan nama bot yang sudah diset"""
        return self.info_message.format(bot_name=self.bot_name)
    
    def add_admin(self, user_id: int) -> None:
        """Tambah admin baru"""
        if user_id not in self.admin_ids:
            self.admin_ids.append(user_id)
    
    def remove_admin(self, user_id: int) -> None:
        """Hapus admin"""
        if user_id in self.admin_ids:
            self.admin_ids.remove(user_id)
    
    def is_admin(self, user_id: int) -> bool:
        """Cek apakah user adalah admin"""
        return user_id in self.admin_ids

# Instance global konfigurasi
config = BotConfig()