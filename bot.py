import asyncio
import logging
import os
from telethon import TelegramClient, events
from fastapi import FastAPI

API_ID = 38036402
API_HASH = "c11ba405e629262a728eadce550b94f8"
BOT_TOKEN = "9066924866:AAG0pZxQRvYGCl6v1noL0HIPV5vG9BFs6NY"

user_client = TelegramClient('session_upravlyalka', API_ID, API_HASH)
bot_client = TelegramClient('bot_bridge', API_ID, API_HASH)

logging.basicConfig(level=logging.INFO)
app = FastAPI()

@app.get("/")
async def root(): 
    return {"status": "Мост авторизации запущен!"}

# Твой номер телефона намертво вшит в код
phone_number = "+380957708743"
phone_code_hash = None

@bot_client.on(events.NewMessage(pattern='/start'))
async def start(event):
    global phone_code_hash
    await event.reply("🚀 Начинаю авторизацию...\nОтправляю запрос кода в Телеграм...")
    try:
        await user_client.connect()
        send_code_res = await user_client.send_code_request(phone_number)
        phone_code_hash = send_code_res.phone_code_hash
        await event.reply("📩 Код отправлен! Напиши мне его прямо сюда в ответ следующим сообщением (просто цифры).")
    except Exception as e:
        await event.reply(f"❌ Ошибка запроса: {e}")

@bot_client.on(events.NewMessage())
async def handle_code(event):
    global phone_code_hash
    if event.text.startswith('/'): 
        return
    if phone_code_hash:
        code = event.text.strip()
        await event.reply(f"Пытаюсь войти с кодом {code}...")
        try:
            await user_client.sign_in(phone_number, code, phone_code_hash=phone_code_hash)
            await event.reply("👑 ПОБЕДА! Юзербот успешно вошел в аккаунт! Сессия сохранена на сервере.")
        except Exception as e:
            await event.reply(f"❌ Ошибка входа: {e}")

@app.on_event("startup")
async def on_startup():
    await bot_client.start(bot_token=BOT_TOKEN)
    await user_client.connect()
    print("Мост готов!")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
