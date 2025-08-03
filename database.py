"""
Database Module untuk Bot Telegram
Mengelola data user, langganan, dan admin
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Kelas untuk mengelola database bot"""
    
    def __init__(self, db_path: str = "bot_database.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inisialisasi database dan buat tabel jika belum ada"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Tabel users untuk data pengguna
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1,
                        subscription_status TEXT DEFAULT 'free',
                        expired_date TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabel subscriptions untuk riwayat langganan
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS subscriptions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        subscription_type TEXT,
                        duration_days INTEGER,
                        start_date TIMESTAMP,
                        end_date TIMESTAMP,
                        status TEXT DEFAULT 'active',
                        created_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')
                
                # Tabel admin_actions untuk log aktivitas admin
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admin_actions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin_id INTEGER,
                        action_type TEXT,
                        target_user_id INTEGER,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabel notifications untuk notifikasi yang sudah dikirim
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS notifications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        notification_type TEXT,
                        message TEXT,
                        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')
                
                conn.commit()
                logger.info("Database berhasil diinisialisasi")
                
        except Exception as e:
            logger.error(f"Error inisialisasi database: {e}")
            raise
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None) -> bool:
        """Tambah user baru ke database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO users 
                    (user_id, username, first_name, last_name, updated_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (user_id, username, first_name, last_name))
                conn.commit()
                logger.info(f"User {user_id} berhasil ditambahkan/diupdate")
                return True
        except Exception as e:
            logger.error(f"Error menambah user {user_id}: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Dapatkan data user berdasarkan user_id"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM users WHERE user_id = ?
                ''', (user_id,))
                row = cursor.fetchone()
                
                if row:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, row))
                return None
        except Exception as e:
            logger.error(f"Error mengambil data user {user_id}: {e}")
            return None
    
    def update_user_subscription(self, user_id: int, subscription_type: str, duration_days: int, admin_id: int = None) -> bool:
        """Update langganan user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Hitung tanggal expired
                current_date = datetime.now()
                expired_date = current_date + timedelta(days=duration_days)
                
                # Update user
                cursor.execute('''
                    UPDATE users 
                    SET subscription_status = ?, expired_date = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (subscription_type, expired_date, user_id))
                
                # Tambah riwayat langganan
                cursor.execute('''
                    INSERT INTO subscriptions 
                    (user_id, subscription_type, duration_days, start_date, end_date, created_by)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, subscription_type, duration_days, current_date, expired_date, admin_id))
                
                # Log admin action
                if admin_id:
                    cursor.execute('''
                        INSERT INTO admin_actions 
                        (admin_id, action_type, target_user_id, description)
                        VALUES (?, ?, ?, ?)
                    ''', (admin_id, 'extend_subscription', user_id, f'Perpanjang langganan {duration_days} hari'))
                
                conn.commit()
                logger.info(f"Langganan user {user_id} berhasil diperpanjang {duration_days} hari")
                return True
                
        except Exception as e:
            logger.error(f"Error update langganan user {user_id}: {e}")
            return False
    
    def get_expiring_subscriptions(self, days_threshold: int = 1) -> List[Dict[str, Any]]:
        """Dapatkan user yang langganannya akan habis dalam X hari"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                threshold_date = datetime.now() + timedelta(days=days_threshold)
                
                cursor.execute('''
                    SELECT user_id, username, first_name, expired_date
                    FROM users 
                    WHERE expired_date <= ? 
                    AND subscription_status != 'free'
                    AND is_active = 1
                ''', (threshold_date,))
                
                rows = cursor.fetchall()
                return [
                    {
                        'user_id': row[0],
                        'username': row[1],
                        'first_name': row[2],
                        'expired_date': row[3]
                    }
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"Error mengambil data langganan yang akan habis: {e}")
            return []
    
    def get_expired_subscriptions(self) -> List[Dict[str, Any]]:
        """Dapatkan user yang langganannya sudah habis"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                current_date = datetime.now()
                
                cursor.execute('''
                    SELECT user_id, username, first_name, expired_date
                    FROM users 
                    WHERE expired_date < ? 
                    AND subscription_status != 'free'
                    AND is_active = 1
                ''', (current_date,))
                
                rows = cursor.fetchall()
                return [
                    {
                        'user_id': row[0],
                        'username': row[1],
                        'first_name': row[2],
                        'expired_date': row[3]
                    }
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"Error mengambil data langganan yang sudah habis: {e}")
            return []
    
    def add_notification_log(self, user_id: int, notification_type: str, message: str) -> bool:
        """Tambah log notifikasi yang sudah dikirim"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO notifications (user_id, notification_type, message)
                    VALUES (?, ?, ?)
                ''', (user_id, notification_type, message))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error menambah log notifikasi: {e}")
            return False
    
    def get_subscription_status(self, user_id: int) -> Dict[str, Any]:
        """Dapatkan status langganan user"""
        try:
            user = self.get_user(user_id)
            if not user:
                return {'status': 'not_found', 'message': 'User tidak ditemukan'}
            
            if user['subscription_status'] == 'free':
                return {'status': 'free', 'message': 'Akun gratis'}
            
            if not user['expired_date']:
                return {'status': 'no_expiry', 'message': 'Tidak ada tanggal expired'}
            
            expired_date = datetime.fromisoformat(user['expired_date'])
            current_date = datetime.now()
            
            if expired_date < current_date:
                days_expired = (current_date - expired_date).days
                return {
                    'status': 'expired',
                    'message': f'Langganan habis {days_expired} hari yang lalu',
                    'expired_date': expired_date,
                    'days_expired': days_expired
                }
            else:
                days_remaining = (expired_date - current_date).days
                return {
                    'status': 'active',
                    'message': f'Langganan aktif, tersisa {days_remaining} hari',
                    'expired_date': expired_date,
                    'days_remaining': days_remaining
                }
                
        except Exception as e:
            logger.error(f"Error cek status langganan user {user_id}: {e}")
            return {'status': 'error', 'message': 'Error sistem'}
    
    def get_all_users(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Dapatkan semua user (untuk admin)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_id, username, first_name, subscription_status, expired_date, joined_date
                    FROM users 
                    ORDER BY joined_date DESC 
                    LIMIT ?
                ''', (limit,))
                
                rows = cursor.fetchall()
                return [
                    {
                        'user_id': row[0],
                        'username': row[1],
                        'first_name': row[2],
                        'subscription_status': row[3],
                        'expired_date': row[4],
                        'joined_date': row[5]
                    }
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"Error mengambil data semua user: {e}")
            return []
    
    def get_admin_actions(self, admin_id: int = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Dapatkan log aktivitas admin"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if admin_id:
                    cursor.execute('''
                        SELECT * FROM admin_actions 
                        WHERE admin_id = ?
                        ORDER BY created_at DESC 
                        LIMIT ?
                    ''', (admin_id, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM admin_actions 
                        ORDER BY created_at DESC 
                        LIMIT ?
                    ''', (limit,))
                
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Error mengambil log admin actions: {e}")
            return []

# Instance global database manager
db_manager = DatabaseManager()