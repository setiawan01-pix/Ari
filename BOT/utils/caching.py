from .data_manager import load_user_data, save_user_data, load_customization_data, save_customization_data, load_prices_data, save_prices_data

_user_data_cache = None
_customization_data_cache = None
_prices_data_cache = None

def get_user_data():
    global _user_data_cache
    if _user_data_cache is None:
        _user_data_cache = load_user_data()
    return _user_data_cache

def update_user_data(new_data):
    global _user_data_cache
    _user_data_cache = new_data
    save_user_data(new_data)

def get_customization_data():
    global _customization_data_cache
    if _customization_data_cache is None:
        _customization_data_cache = load_customization_data()
    return _customization_data_cache

def update_customization_data(new_data):
    global _customization_data_cache
    _customization_data_cache = new_data
    save_customization_data(new_data)

def get_prices_data():
    global _prices_data_cache
    if _prices_data_cache is None:
        _prices_data_cache = load_prices_data()
    return _prices_data_cache

def update_prices_data(new_data):
    global _prices_data_cache
    _prices_data_cache = new_data
    save_prices_data(new_data)
