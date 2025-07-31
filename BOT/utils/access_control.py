from datetime import datetime
from utils.caching import get_user_data

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
            return "expired"
        else:
            return "trial"

    elif status == "premium":
        # Premium logic can be expanded here if needed (e.g., subscription tiers)
        return "premium"

    return "unknown"
