import json
import os
from typing import Dict, Any

def get_customization_data() -> Dict[str, Any]:
    """Get customization data from JSON file"""
    customization_file = "customization.json"
    
    if os.path.exists(customization_file):
        try:
            with open(customization_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    # Default customization
    default_data = {
        "welcome_message": "🔐 SISTEM AKSES USER\n\n🧪 Trial 1 Jam\n🔐 Premium (Berbayar)\nℹ️ Info Bot\n\nTrial: aktif 1jam → auto expired\nPremium: tampilkan harga + QR → admin aktifkan",
        "payment_method": "Transfer Bank",
        "qr_code_path": None,
        "prices": {
            "1_hari": 5000,
            "7_hari": 25000,
            "30_hari": 75000,
            "lifetime": 200000
        }
    }
    
    # Save default data
    save_customization_data(default_data)
    return default_data

def save_customization_data(data: Dict[str, Any]):
    """Save customization data to JSON file"""
    customization_file = "customization.json"
    
    with open(customization_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_welcome_message(message: str):
    """Update welcome message"""
    data = get_customization_data()
    data["welcome_message"] = message
    save_customization_data(data)

def update_payment_method(method: str):
    """Update payment method"""
    data = get_customization_data()
    data["payment_method"] = method
    save_customization_data(data)

def update_qr_code_path(path: str):
    """Update QR code path"""
    data = get_customization_data()
    data["qr_code_path"] = path
    save_customization_data(data)

def update_prices(prices: Dict[str, int]):
    """Update prices"""
    data = get_customization_data()
    data["prices"] = prices
    save_customization_data(data)
