from datetime import datetime

LOG_FILE = "log.txt"

def log_activity(user_id, activity):
    """Logs user activity."""
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] ID:{user_id} ➝ {activity}\n")
