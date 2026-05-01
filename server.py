# ─── سرور اصلی ───────────────────────────────────────────
import os
import requests
from flask import Flask, request
from groq import Groq
from config import (GROQ_API_KEY, GROQ_MODEL, WA_TOKEN,
                    WA_PHONE_ID, WA_VERIFY_TOKEN, BUSINESS_NAME)

app = Flask(__name__)
groq_client = Groq(api_key=GROQ_API_KEY)

# حافظه مکالمات
conversations = {}


def safe_load_inventory():
    try:
        from agent import load_inventory
        return load_inventory()
    except:
        return []


def get_inventory_text():
    inventory = safe_load_inventory()
    if not inventory:
        return "موجودی در دسترس نیست"
    text = ""
    for item in inventory:
        text += f"- {item['name']}: {item['price']:,} تومان\n"
    return text


def chat_with_ai(phone, user_message):
    if phone not in conversations:
        conversations[phone] = []

    inventory_text = get_inventory_text()

    system_prompt = f"""تو یه دستیار فروش هوشمند برای {BUSINESS_NAME} هستی.
با مشتریان به فارسی صحبت کن، دوستانه و صمیمی باش.
اگه مشتری رسمی بود رسمی جواب بده، اگه شوخی کرد شوخی کن.
هرگز نگو که AI یا ربات هستی.

موجودی فعلی:
{inventory_text}

قوانین:
- فقط کالاهای موجود رو پیشنهاد بده
- قیمت‌ها رو دقیق بگو
- اگه کالایی نداری صادق باش
- پیام‌ها رو کوتاه و مفید نگه دار"""

    conversations[phone].append({
        "role": "user",
        "content": user_message
    })

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            *conversations[phone]
        ],
        max_tokens=500
    )

    ai_reply = response.choices[0].message.content
    conversations[phone].append({
        "role": "assistant",
        "content": ai_reply
    })

    return ai_reply


def send_whatsapp_message(phone, message):
    url = f"https://graph.facebook.com/v19.0/{WA_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=payload)


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == WA_VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.json

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "messages" not in value:
            return "ok", 200

        message = value["messages"][0]
        phone = message["from"]
        text = message["text"]["body"]

        print(f"پیام از {phone}: {text}")

        ai_reply = chat_with_ai(phone, text)
        send_whatsapp_message(phone, ai_reply)

        print(f"جواب به {phone}: {ai_reply}")

    except Exception as e:
        print(f"خطا: {e}")

    return "ok", 200


@app.route("/")
def home():
    return "ایجنت فروش آنلاین است", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)