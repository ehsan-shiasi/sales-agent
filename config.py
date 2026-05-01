import os

# نام کسب‌وکار
BUSINESS_NAME = "فروشگاه من"

# Groq API
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL   = "llama-3.3-70b-versatile"

# واتساپ (بعداً پر می‌کنیم)
WA_TOKEN        = os.environ.get("WA_TOKEN", "")
WA_PHONE_ID     = os.environ.get("WA_PHONE_ID", "")
WA_VERIFY_TOKEN = os.environ.get("WA_VERIFY_TOKEN", "my_secret_verify_token")

# فایل‌های داده
CUSTOMERS_FILE = "data/customers.xlsx"
INVENTORY_FILE = "data/inventory.xlsx"

# تنظیمات ایجنت
MAX_SUGGESTIONS = 3