# ─── فایل اجرایی اصلی ───────────────────────────────────
import time
from agent import load_customers, load_inventory, find_suggestions, build_message
from whatsapp import send_text
from config import BUSINESS_NAME

def run():
    print("=" * 50)
    print("  ایجنت فروش هوشمند - شروع")
    print("=" * 50)

    print("\n  در حال بارگذاری داده‌ها...")
    customers = load_customers()
    inventory = load_inventory()

    print(f"  {len(customers)} مشتری یافت شد")
    print(f"  {len(inventory)} کالا در موجودی")
    print()

    input("  برای شروع ارسال Enter بزن...")
    print()

    total   = len(customers)
    success = 0
    failed  = 0

    for i, (name, info) in enumerate(customers.items(), 1):
        suggestions = find_suggestions(info["history"], inventory)

        if not suggestions:
            print(f"[{i}/{total}]  پیشنهادی برای {name} نبود - رد شد")
            continue

        print(f"[{i}/{total}]  در حال ارسال به: {name} ({info['phone']})")

        msg = build_message(name, info["history"], suggestions)
        ok  = send_text(info["phone"], msg)

        if ok:
            success += 1
        else:
            failed += 1

        time.sleep(2)

    print()
    print("=" * 50)
    print(f"  تمام! موفق: {success} | ناموفق: {failed}")
    print("=" * 50)
    input("\n  Enter بزن تا بسته بشه...")

if __name__ == "__main__":
    run()