from datetime import datetime
from utils.caching import get_user_data, update_user_data

def get_user_status(user_id):
    user_data = get_user_data()
    user_id = str(user_id)

    if user_id not in user_data:
        return "not_registered"

    user = user_data[user_id]
    status = user.get("status")

    if status == "trial":
        expire_time = datetime.fromisoformat(user.get("expire_time"))
        if datetime.now() > expire_time:
            # Auto-cleanup expired trial
            user_data[user_id]["status"] = "expired"
            update_user_data(user_data)
            return "expired"
        else:
            return "trial"

    elif status == "premium":
        # Premium logic can be expanded here if needed (e.g., subscription tiers)
        expire_time_str = user.get("expire_time")
        if expire_time_str:
            expire_time = datetime.fromisoformat(expire_time_str)
            if datetime.now() > expire_time:
                user_data[user_id]["status"] = "expired"
                update_user_data(user_data)
                return "expired"
        return "premium"
    
    elif status == "expired":
        return "expired"

    return "unknown"
