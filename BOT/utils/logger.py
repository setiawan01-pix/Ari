import os
from datetime import datetime
from config import LOG_FILE

def log_activity(user_id: int, action: str, details: str = ""):
    """Log user activity to log file"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} ID:{user_id} ➝ {action}"
    
    if details:
        log_entry += f" - {details}"
    
    log_entry += "\n"
    
    # Ensure log directory exists
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Append to log file
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def get_recent_logs(lines: int = 50) -> str:
    """Get recent log entries"""
    if not os.path.exists(LOG_FILE):
        return "Log file tidak ditemukan."
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
        
        # Get last N lines
        recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        return ''.join(recent_lines)
    except Exception as e:
        return f"Error membaca log: {str(e)}"

def clear_logs():
    """Clear all logs"""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
