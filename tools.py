"""
Tools Module untuk Bot Telegram
Berisi fitur konversi dan utilitas lainnya
"""

import re
import json
import hashlib
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class ConversionTools:
    """Kelas untuk fitur konversi"""
    
    @staticmethod
    def text_to_base64(text: str) -> str:
        """Konversi teks ke Base64"""
        try:
            encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            return encoded
        except Exception as e:
            logger.error(f"Error konversi text ke base64: {e}")
            return "Error: Gagal mengkonversi teks"
    
    @staticmethod
    def base64_to_text(base64_string: str) -> str:
        """Konversi Base64 ke teks"""
        try:
            decoded = base64.b64decode(base64_string.encode('utf-8')).decode('utf-8')
            return decoded
        except Exception as e:
            logger.error(f"Error konversi base64 ke text: {e}")
            return "Error: Gagal mengkonversi Base64"
    
    @staticmethod
    def text_to_md5(text: str) -> str:
        """Konversi teks ke MD5 hash"""
        try:
            md5_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
            return md5_hash
        except Exception as e:
            logger.error(f"Error konversi text ke MD5: {e}")
            return "Error: Gagal mengkonversi ke MD5"
    
    @staticmethod
    def text_to_sha256(text: str) -> str:
        """Konversi teks ke SHA256 hash"""
        try:
            sha256_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
            return sha256_hash
        except Exception as e:
            logger.error(f"Error konversi text ke SHA256: {e}")
            return "Error: Gagal mengkonversi ke SHA256"
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Konversi Celsius ke Fahrenheit"""
        try:
            fahrenheit = (celsius * 9/5) + 32
            return round(fahrenheit, 2)
        except Exception as e:
            logger.error(f"Error konversi celsius ke fahrenheit: {e}")
            return 0.0
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Konversi Fahrenheit ke Celsius"""
        try:
            celsius = (fahrenheit - 32) * 5/9
            return round(celsius, 2)
        except Exception as e:
            logger.error(f"Error konversi fahrenheit ke celsius: {e}")
            return 0.0
    
    @staticmethod
    def km_to_miles(km: float) -> float:
        """Konversi Kilometer ke Miles"""
        try:
            miles = km * 0.621371
            return round(miles, 2)
        except Exception as e:
            logger.error(f"Error konversi km ke miles: {e}")
            return 0.0
    
    @staticmethod
    def miles_to_km(miles: float) -> float:
        """Konversi Miles ke Kilometer"""
        try:
            km = miles * 1.60934
            return round(km, 2)
        except Exception as e:
            logger.error(f"Error konversi miles ke km: {e}")
            return 0.0
    
    @staticmethod
    def kg_to_lbs(kg: float) -> float:
        """Konversi Kilogram ke Pounds"""
        try:
            lbs = kg * 2.20462
            return round(lbs, 2)
        except Exception as e:
            logger.error(f"Error konversi kg ke lbs: {e}")
            return 0.0
    
    @staticmethod
    def lbs_to_kg(lbs: float) -> float:
        """Konversi Pounds ke Kilogram"""
        try:
            kg = lbs * 0.453592
            return round(kg, 2)
        except Exception as e:
            logger.error(f"Error konversi lbs ke kg: {e}")
            return 0.0

class TextTools:
    """Kelas untuk tools teks"""
    
    @staticmethod
    def count_characters(text: str) -> Dict[str, int]:
        """Hitung karakter dalam teks"""
        try:
            return {
                'total_chars': len(text),
                'total_words': len(text.split()),
                'total_lines': len(text.splitlines()),
                'spaces': text.count(' '),
                'letters': len(re.findall(r'[a-zA-Z]', text)),
                'numbers': len(re.findall(r'\d', text)),
                'special_chars': len(re.findall(r'[^a-zA-Z0-9\s]', text))
            }
        except Exception as e:
            logger.error(f"Error menghitung karakter: {e}")
            return {}
    
    @staticmethod
    def reverse_text(text: str) -> str:
        """Balik urutan teks"""
        try:
            return text[::-1]
        except Exception as e:
            logger.error(f"Error membalik teks: {e}")
            return "Error: Gagal membalik teks"
    
    @staticmethod
    def uppercase_text(text: str) -> str:
        """Konversi teks ke huruf besar"""
        try:
            return text.upper()
        except Exception as e:
            logger.error(f"Error konversi ke uppercase: {e}")
            return "Error: Gagal mengkonversi ke uppercase"
    
    @staticmethod
    def lowercase_text(text: str) -> str:
        """Konversi teks ke huruf kecil"""
        try:
            return text.lower()
        except Exception as e:
            logger.error(f"Error konversi ke lowercase: {e}")
            return "Error: Gagal mengkonversi ke lowercase"
    
    @staticmethod
    def title_case_text(text: str) -> str:
        """Konversi teks ke title case"""
        try:
            return text.title()
        except Exception as e:
            logger.error(f"Error konversi ke title case: {e}")
            return "Error: Gagal mengkonversi ke title case"
    
    @staticmethod
    def remove_spaces(text: str) -> str:
        """Hapus semua spasi dari teks"""
        try:
            return text.replace(" ", "")
        except Exception as e:
            logger.error(f"Error menghapus spasi: {e}")
            return "Error: Gagal menghapus spasi"

class DateTimeTools:
    """Kelas untuk tools tanggal dan waktu"""
    
    @staticmethod
    def get_current_time() -> Dict[str, str]:
        """Dapatkan waktu saat ini dalam berbagai format"""
        try:
            now = datetime.now()
            return {
                'datetime': now.strftime('%Y-%m-%d %H:%M:%S'),
                'date': now.strftime('%d/%m/%Y'),
                'time': now.strftime('%H:%M:%S'),
                'timestamp': str(int(now.timestamp())),
                'iso': now.isoformat(),
                'formatted': now.strftime('%A, %d %B %Y %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"Error mendapatkan waktu: {e}")
            return {}
    
    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> str:
        """Konversi timestamp ke datetime"""
        try:
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logger.error(f"Error konversi timestamp: {e}")
            return "Error: Gagal mengkonversi timestamp"
    
    @staticmethod
    def datetime_to_timestamp(datetime_str: str) -> str:
        """Konversi datetime string ke timestamp"""
        try:
            dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            return str(int(dt.timestamp()))
        except Exception as e:
            logger.error(f"Error konversi datetime: {e}")
            return "Error: Gagal mengkonversi datetime"

class JSONTools:
    """Kelas untuk tools JSON"""
    
    @staticmethod
    def format_json(json_string: str) -> str:
        """Format JSON string agar mudah dibaca"""
        try:
            parsed = json.loads(json_string)
            return json.dumps(parsed, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error format JSON: {e}")
            return "Error: JSON tidak valid"
    
    @staticmethod
    def minify_json(json_string: str) -> str:
        """Minify JSON string"""
        try:
            parsed = json.loads(json_string)
            return json.dumps(parsed, separators=(',', ':'))
        except Exception as e:
            logger.error(f"Error minify JSON: {e}")
            return "Error: JSON tidak valid"
    
    @staticmethod
    def validate_json(json_string: str) -> Dict[str, Any]:
        """Validasi JSON string"""
        try:
            parsed = json.loads(json_string)
            return {
                'valid': True,
                'type': type(parsed).__name__,
                'size': len(json_string)
            }
        except json.JSONDecodeError as e:
            return {
                'valid': False,
                'error': str(e),
                'line': e.lineno,
                'column': e.colno
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }

class CalculatorTools:
    """Kelas untuk kalkulator sederhana"""
    
    @staticmethod
    def calculate(expression: str) -> str:
        """Kalkulasi ekspresi matematika sederhana"""
        try:
            # Bersihkan ekspresi
            expression = expression.replace(' ', '')
            
            # Validasi karakter yang diizinkan
            allowed_chars = set('0123456789+-*/().')
            if not all(c in allowed_chars for c in expression):
                return "Error: Karakter tidak diizinkan"
            
            # Evaluasi ekspresi
            result = eval(expression)
            
            # Format hasil
            if isinstance(result, (int, float)):
                if result == int(result):
                    return str(int(result))
                else:
                    return str(round(result, 4))
            else:
                return str(result)
                
        except ZeroDivisionError:
            return "Error: Pembagian dengan nol"
        except Exception as e:
            logger.error(f"Error kalkulasi: {e}")
            return "Error: Ekspresi tidak valid"

class URLTools:
    """Kelas untuk tools URL"""
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Ekstrak URL dari teks"""
        try:
            url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
            urls = re.findall(url_pattern, text)
            return urls
        except Exception as e:
            logger.error(f"Error ekstrak URL: {e}")
            return []
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Cek apakah URL valid"""
        try:
            url_pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
            return bool(re.match(url_pattern, url))
        except Exception as e:
            logger.error(f"Error validasi URL: {e}")
            return False

# Instance global tools
conversion_tools = ConversionTools()
text_tools = TextTools()
datetime_tools = DateTimeTools()
json_tools = JSONTools()
calculator_tools = CalculatorTools()
url_tools = URLTools()