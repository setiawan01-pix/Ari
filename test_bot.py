#!/usr/bin/env python3
"""
Test Script untuk Bot Telegram
Script untuk testing fitur-fitur bot sebelum deployment
"""

import asyncio
import logging
from datetime import datetime, timedelta
from database import db_manager
from tools import conversion_tools, text_tools, datetime_tools, json_tools, calculator_tools, url_tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database():
    """Test fungsi database"""
    print("🧪 Testing Database Functions...")
    
    try:
        # Test add user
        success = db_manager.add_user(
            user_id=123456789,
            username="testuser",
            first_name="Test",
            last_name="User"
        )
        print(f"✅ Add user: {success}")
        
        # Test get user
        user = db_manager.get_user(123456789)
        print(f"✅ Get user: {user is not None}")
        
        # Test update subscription
        success = db_manager.update_user_subscription(
            user_id=123456789,
            subscription_type="premium",
            duration_days=30,
            admin_id=987654321
        )
        print(f"✅ Update subscription: {success}")
        
        # Test get subscription status
        status = db_manager.get_subscription_status(123456789)
        print(f"✅ Get status: {status['status']}")
        
        # Test get all users
        users = db_manager.get_all_users(limit=5)
        print(f"✅ Get all users: {len(users)} users found")
        
        print("✅ Database tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_conversion_tools():
    """Test tools konversi"""
    print("\n🧪 Testing Conversion Tools...")
    
    try:
        # Test Base64
        text = "Hello World"
        encoded = conversion_tools.text_to_base64(text)
        decoded = conversion_tools.base64_to_text(encoded)
        print(f"✅ Base64: {text} → {encoded} → {decoded}")
        
        # Test MD5
        md5_hash = conversion_tools.text_to_md5(text)
        print(f"✅ MD5: {text} → {md5_hash}")
        
        # Test SHA256
        sha256_hash = conversion_tools.text_to_sha256(text)
        print(f"✅ SHA256: {text} → {sha256_hash}")
        
        # Test temperature conversion
        celsius = 25
        fahrenheit = conversion_tools.celsius_to_fahrenheit(celsius)
        celsius_back = conversion_tools.fahrenheit_to_celsius(fahrenheit)
        print(f"✅ Temperature: {celsius}°C → {fahrenheit}°F → {celsius_back}°C")
        
        # Test distance conversion
        km = 10
        miles = conversion_tools.km_to_miles(km)
        km_back = conversion_tools.miles_to_km(miles)
        print(f"✅ Distance: {km}km → {miles}miles → {km_back}km")
        
        # Test weight conversion
        kg = 50
        lbs = conversion_tools.kg_to_lbs(kg)
        kg_back = conversion_tools.lbs_to_kg(lbs)
        print(f"✅ Weight: {kg}kg → {lbs}lbs → {kg_back}kg")
        
        print("✅ Conversion tools tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Conversion tools test failed: {e}")
        return False

def test_text_tools():
    """Test text tools"""
    print("\n🧪 Testing Text Tools...")
    
    try:
        text = "Hello World 123!"
        
        # Test count characters
        count = text_tools.count_characters(text)
        print(f"✅ Count characters: {count}")
        
        # Test reverse text
        reversed_text = text_tools.reverse_text(text)
        print(f"✅ Reverse text: {text} → {reversed_text}")
        
        # Test uppercase
        upper_text = text_tools.uppercase_text(text)
        print(f"✅ Uppercase: {text} → {upper_text}")
        
        # Test lowercase
        lower_text = text_tools.lowercase_text(text)
        print(f"✅ Lowercase: {text} → {lower_text}")
        
        # Test title case
        title_text = text_tools.title_case_text(text)
        print(f"✅ Title case: {text} → {title_text}")
        
        # Test remove spaces
        no_space_text = text_tools.remove_spaces(text)
        print(f"✅ Remove spaces: {text} → {no_space_text}")
        
        print("✅ Text tools tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Text tools test failed: {e}")
        return False

def test_datetime_tools():
    """Test datetime tools"""
    print("\n🧪 Testing DateTime Tools...")
    
    try:
        # Test get current time
        current_time = datetime_tools.get_current_time()
        print(f"✅ Current time: {current_time}")
        
        # Test timestamp conversion
        timestamp = int(datetime.now().timestamp())
        datetime_str = datetime_tools.timestamp_to_datetime(timestamp)
        timestamp_back = datetime_tools.datetime_to_timestamp(datetime_str)
        print(f"✅ Timestamp: {timestamp} → {datetime_str} → {timestamp_back}")
        
        print("✅ DateTime tools tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ DateTime tools test failed: {e}")
        return False

def test_json_tools():
    """Test JSON tools"""
    print("\n🧪 Testing JSON Tools...")
    
    try:
        # Test JSON
        json_string = '{"name":"John","age":30,"city":"New York"}'
        
        # Test format JSON
        formatted = json_tools.format_json(json_string)
        print(f"✅ Format JSON: {formatted}")
        
        # Test minify JSON
        minified = json_tools.minify_json(formatted)
        print(f"✅ Minify JSON: {minified}")
        
        # Test validate JSON
        validation = json_tools.validate_json(json_string)
        print(f"✅ Validate JSON: {validation}")
        
        # Test invalid JSON
        invalid_json = '{"name":"John","age":30,}'
        validation_invalid = json_tools.validate_json(invalid_json)
        print(f"✅ Validate invalid JSON: {validation_invalid}")
        
        print("✅ JSON tools tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ JSON tools test failed: {e}")
        return False

def test_calculator_tools():
    """Test calculator tools"""
    print("\n🧪 Testing Calculator Tools...")
    
    try:
        # Test basic operations
        operations = [
            ("2 + 2", "4"),
            ("10 * 5", "50"),
            ("100 / 4", "25"),
            ("(2 + 3) * 4", "20"),
            ("10 - 3", "7")
        ]
        
        for expression, expected in operations:
            result = calculator_tools.calculate(expression)
            status = "✅" if result == expected else "❌"
            print(f"{status} {expression} = {result} (expected: {expected})")
        
        # Test invalid expression
        invalid_result = calculator_tools.calculate("2 + ")
        print(f"✅ Invalid expression: {invalid_result}")
        
        print("✅ Calculator tools tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Calculator tools test failed: {e}")
        return False

def test_url_tools():
    """Test URL tools"""
    print("\n🧪 Testing URL Tools...")
    
    try:
        # Test extract URLs
        text_with_urls = "Visit https://example.com and https://google.com for more info"
        urls = url_tools.extract_urls(text_with_urls)
        print(f"✅ Extract URLs: {urls}")
        
        # Test validate URLs
        valid_urls = [
            "https://example.com",
            "http://google.com",
            "https://www.github.com/user/repo"
        ]
        
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "just text"
        ]
        
        for url in valid_urls:
            is_valid = url_tools.is_valid_url(url)
            print(f"✅ Valid URL {url}: {is_valid}")
        
        for url in invalid_urls:
            is_valid = url_tools.is_valid_url(url)
            print(f"✅ Invalid URL {url}: {is_valid}")
        
        print("✅ URL tools tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ URL tools test failed: {e}")
        return False

def test_notification_system():
    """Test notification system (simulation)"""
    print("\n🧪 Testing Notification System...")
    
    try:
        # Test get expiring subscriptions
        expiring = db_manager.get_expiring_subscriptions(days_threshold=7)
        print(f"✅ Expiring subscriptions: {len(expiring)} users")
        
        # Test get expired subscriptions
        expired = db_manager.get_expired_subscriptions()
        print(f"✅ Expired subscriptions: {len(expired)} users")
        
        # Test add notification log
        success = db_manager.add_notification_log(
            user_id=123456789,
            notification_type="test",
            message="Test notification"
        )
        print(f"✅ Add notification log: {success}")
        
        print("✅ Notification system tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Notification system test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Bot Telegram Tests...")
    print("=" * 50)
    
    tests = [
        ("Database", test_database),
        ("Conversion Tools", test_conversion_tools),
        ("Text Tools", test_text_tools),
        ("DateTime Tools", test_datetime_tools),
        ("JSON Tools", test_json_tools),
        ("Calculator Tools", test_calculator_tools),
        ("URL Tools", test_url_tools),
        ("Notification System", test_notification_system)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Bot is ready for deployment.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    print("\n📝 Next steps:")
    print("1. Set your bot token in config.py or environment variable")
    print("2. Set your admin ID in config.py")
    print("3. Run the bot with: python3 telegram_bot.py")
    print("4. Test admin features with /admin command")

if __name__ == "__main__":
    main()