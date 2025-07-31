import json

USER_DATA_FILE = "BOT/user_data.json"
CUSTOMIZATION_FILE = "BOT/customization.json"
PRICES_FILE = "BOT/prices.json"

def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_customization_data():
    try:
        with open(CUSTOMIZATION_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_customization_data(data):
    with open(CUSTOMIZATION_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_prices_data():
    try:
        with open(PRICES_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_prices_data(data):
    with open(PRICES_FILE, "w") as f:
        json.dump(data, f, indent=4)
