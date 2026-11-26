
import os
import time
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL_ID"]

API = f"https://api.telegram.org/bot{TOKEN}"
TARGET = datetime(2027, 9, 1, 0, 0, 0,
                  tzinfo=ZoneInfo("Asia/Tashkent"))

def countdown():
    now = datetime.now(ZoneInfo("Asia/Tashkent"))
    remaining = max(0, int((TARGET - now).total_seconds()))

    days, remaining = divmod(remaining, 86400)
    hours, remaining = divmod(remaining, 3600)
    minutes, seconds = divmod(remaining, 60)

    return (
        "💍 <b>OUR SPECIAL DAY</b>\n\n"
        "❤️ <b>1 SENTYABR 2027</b>\n\n"
        f"💎 {days} kun\n"
        f"🕒 {hours:02d} soat\n"
        f"⏳ {minutes:02d} daqiqa\n"
        f"✨ {seconds:02d} soniya\n\n"
        "❤️ <i>Har bir soniya yaqinlashtiradi...</i>"
    )

def call(method, data):
    response = requests.post(
        f"{API}/{method}", data=data, timeout=20
    )
    response.raise_for_status()
    result = response.json()
    if not result.get("ok"):
        raise Exception(result)
    return result["result"]

message_id = None

while True:
    try:
        if message_id is None:
            result = call("sendMessage", {
                "chat_id": CHANNEL,
                "text": countdown(),
                "parse_mode": "HTML"
            })
            message_id = result["message_id"]

            call("pinChatMessage", {
                "chat_id": CHANNEL,
                "message_id": message_id,
                "disable_notification": True
            })
        else:
            call("editMessageText", {
                "chat_id": CHANNEL,
                "message_id": message_id,
                "text": countdown(),
                "parse_mode": "HTML"
            })

        time.sleep(10)

    except Exception as error:
        print("Xatolik:", error)
        time.sleep(30)
