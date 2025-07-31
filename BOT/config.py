import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Use environment variables for sensitive data
TOKEN = os.getenv("BOT_TOKEN", "8198867479:AAEtUhyTID-crNvg8fohpfvTYkYtIEDz6aQ")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8141075788"))

# Warning if using fallback values
if TOKEN == "8198867479:AAEtUhyTID-crNvg8fohpfvTYkYtIEDz6aQ":
    print("⚠️  Warning: Using default BOT_TOKEN. Set BOT_TOKEN in .env file for security!")
    
if ADMIN_ID == 8141075788:
    print("⚠️  Warning: Using default ADMIN_ID. Set ADMIN_ID in .env file!")
