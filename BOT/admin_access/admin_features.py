from BOT.utils.caching import get_user_data, update_user_data, get_customization_data, update_customization_data, get_prices_data, update_prices_data
from telegram.ext import ContextTypes
from telegram import Bot
from BOT.config import TOKEN
from BOT.scheduler import add_scheduled_job
from datetime import datetime

async def broadcast_message(context: ContextTypes.DEFAULT_TYPE, message: str):
    """Broadcasts a message to all users."""
    user_data = get_user_data()
    bot = Bot(TOKEN)
    for user_id in user_data.keys():
        try:
            await bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Could not send message to {user_id}: {e}")

def activate_premium(user_id, days):
    user_data = get_user_data()
    user_id = str(user_id)

    # In a real scenario, you'd calculate the expiration date based on `days`
    user_data[user_id] = {
        "status": "premium",
        "start_time": "N/A",
        "expire_time": "N/A" # Or calculate based on `days`
    }
    update_user_data(user_data)
    return True

def set_payment_method(method):
    data = get_customization_data()
    data["payment_method"] = method
    update_customization_data(data)

def set_qr_code(url):
    data = get_customization_data()
    data["qr_code_url"] = url
    update_customization_data(data)

def set_price(duration, price):
    data = get_prices_data()
    data[duration] = price
    update_prices_data(data)

def schedule_conversion_job(chat_id, run_date_str, file_content, file_name_base, contact_name_base, contacts_per_file, start_order):
    try:
        run_date = datetime.fromisoformat(run_date_str)
        add_scheduled_job(chat_id, run_date, file_content, file_name_base, contact_name_base, contacts_per_file, start_order)
        return True
    except (ValueError, TypeError):
        return False

def get_user_list():
    """Gets a list of all users and their status."""
    user_data = get_user_data()
    user_list = []
    for user_id, data in user_data.items():
        user_list.append(f"ID: {user_id}, Status: {data.get('status')}, Exp: {data.get('expire_time')}")
    return "\n".join(user_list)

def kick_user(user_id):
    """Kicks a user by removing them from the user_data.json."""
    user_data = get_user_data()
    user_id = str(user_id)
    if user_id in user_data:
        del user_data[user_id]
        update_user_data(user_data)
        return True
    return False

def set_welcome_message(message):
    """Sets the welcome message."""
    data = get_customization_data()
    data["welcome_message"] = message
    update_customization_data(data)
