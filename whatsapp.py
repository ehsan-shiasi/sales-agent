# ─── ارتباط با واتساپ ────────────────────────────────────
import requests
from config import WA_TOKEN, WA_PHONE_ID

BASE_URL = f"https://graph.facebook.com/v19.0/{WA_PHONE_ID}"
HEADERS  = {
    "Authorization": f"Bearer {WA_TOKEN}",
    "Content-Type": "application/json"
}


def send_text(phone, message):
    """ارسال پیام متنی"""
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(f"{BASE_URL}/messages", headers=HEADERS, json=payload)
    result = response.json()

    if "messages" in result:
        print(f"  ✅ پیام ارسال شد به {phone}")
        return True
    else:
        error = result.get("error", {}).get("message", "نامشخص")
        print(f"  ❌ خطا: {error}")
        return False


def send_image(phone, image_url, caption):
    """ارسال عکس با کپشن"""
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": caption
        }
    }
    response = requests.post(f"{BASE_URL}/messages", headers=HEADERS, json=payload)
    result = response.json()

    if "messages" in result:
        print(f"  ✅ عکس ارسال شد به {phone}")
        return True
    else:
        error = result.get("error", {}).get("message", "نامشخص")
        print(f"  ❌ خطا در ارسال عکس: {error}")
        return False