import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from config import TRIAL_DURATION_HOURS, PREMIUM_PLANS

class UserManager:
    def __init__(self, user_data_file: str = "user_data.json"):
        self.user_data_file = user_data_file
        self.load_users()
    
    def load_users(self):
        """Load user data from JSON file"""
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            self.save_users()
    
    def save_users(self):
        """Save user data to JSON file"""
        with open(self.user_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=2, ensure_ascii=False)
    
    def get_user(self, user_id: int) -> Dict:
        """Get user data by ID"""
        return self.users.get(str(user_id), {})
    
    def create_user(self, user_id: int, username: str = None) -> Dict:
        """Create new user"""
        user_data = {
            "user_id": user_id,
            "username": username,
            "status": "inactive",
            "created_at": datetime.now().isoformat(),
            "trial_start": None,
            "trial_end": None,
            "premium_start": None,
            "premium_end": None,
            "premium_plan": None
        }
        self.users[str(user_id)] = user_data
        self.save_users()
        return user_data
    
    def activate_trial(self, user_id: int) -> bool:
        """Activate trial for user"""
        user_id_str = str(user_id)
        if user_id_str not in self.users:
            self.create_user(user_id)
        
        user = self.users[user_id_str]
        
        # Check if user already had trial
        if user.get("trial_start"):
            return False
        
        now = datetime.now()
        trial_end = now + timedelta(hours=TRIAL_DURATION_HOURS)
        
        user["status"] = "trial"
        user["trial_start"] = now.isoformat()
        user["trial_end"] = trial_end.isoformat()
        
        self.save_users()
        return True
    
    def activate_premium(self, user_id: int, plan: str, days: int = None) -> bool:
        """Activate premium for user"""
        user_id_str = str(user_id)
        if user_id_str not in self.users:
            self.create_user(user_id)
        
        user = self.users[user_id_str]
        now = datetime.now()
        
        if plan == "lifetime":
            premium_end = None
        else:
            premium_end = now + timedelta(days=days)
        
        user["status"] = "premium"
        user["premium_start"] = now.isoformat()
        user["premium_end"] = premium_end.isoformat() if premium_end else None
        user["premium_plan"] = plan
        
        self.save_users()
        return True
    
    def check_access(self, user_id: int) -> Dict:
        """Check user access status"""
        user_id_str = str(user_id)
        if user_id_str not in self.users:
            return {"has_access": False, "reason": "User not registered"}
        
        user = self.users[user_id_str]
        now = datetime.now()
        
        # Check trial
        if user.get("status") == "trial" and user.get("trial_end"):
            trial_end = datetime.fromisoformat(user["trial_end"])
            if now < trial_end:
                return {"has_access": True, "status": "trial", "expires": trial_end}
            else:
                # Trial expired
                user["status"] = "expired"
                self.save_users()
                return {"has_access": False, "reason": "Trial expired"}
        
        # Check premium
        if user.get("status") == "premium":
            if user.get("premium_plan") == "lifetime":
                return {"has_access": True, "status": "premium", "plan": "lifetime"}
            
            if user.get("premium_end"):
                premium_end = datetime.fromisoformat(user["premium_end"])
                if now < premium_end:
                    return {"has_access": True, "status": "premium", "expires": premium_end}
                else:
                    # Premium expired
                    user["status"] = "expired"
                    self.save_users()
                    return {"has_access": False, "reason": "Premium expired"}
        
        return {"has_access": False, "reason": "No active subscription"}
    
    def get_all_users(self) -> List[Dict]:
        """Get all users for admin panel"""
        users_list = []
        for user_id, user_data in self.users.items():
            access_info = self.check_access(int(user_id))
            user_info = {
                "user_id": user_id,
                "username": user_data.get("username"),
                "status": user_data.get("status"),
                "has_access": access_info["has_access"],
                "created_at": user_data.get("created_at")
            }
            
            if access_info.get("expires"):
                user_info["expires"] = access_info["expires"].isoformat()
            
            users_list.append(user_info)
        
        return users_list
    
    def remove_user(self, user_id: int) -> bool:
        """Remove user from database"""
        user_id_str = str(user_id)
        if user_id_str in self.users:
            del self.users[user_id_str]
            self.save_users()
            return True
        return False
    
    def get_user_stats(self) -> Dict:
        """Get user statistics"""
        total_users = len(self.users)
        trial_users = sum(1 for user in self.users.values() if user.get("status") == "trial")
        premium_users = sum(1 for user in self.users.values() if user.get("status") == "premium")
        expired_users = sum(1 for user in self.users.values() if user.get("status") == "expired")
        
        return {
            "total": total_users,
            "trial": trial_users,
            "premium": premium_users,
            "expired": expired_users
        }

# Global instance
user_manager = UserManager()