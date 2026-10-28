import asyncio
import logging
import os
import random
from datetime import datetime
from telethon import TelegramClient, events
from fastapi import FastAPI

# Твои личные ключи
API_ID = 38036402
API_HASH = "c11ba405e629262a728eadce550b94f8"
BOT_TOKEN = "9066924866:AAG0pZxQRvYGCl6v1noL0HIPV5vG9BFs6NY"

# Создаем только ЮЗЕРКЛИЕНТА, убираем запуск второго бота из стартапа
user_client = TelegramClient('super_clean_session', API_ID, API_HASH)
bot_client = TelegramClient('clean_bridge', API_ID, API_HASH)

logging.basicConfig(level=logging.INFO)
app = FastAPI()

@app.get("/")
async def root(): 
    return {"status": "🚨 ИДЕАЛЬНЫЙ ЗАПУСК! ВСЁ РАБОТАЕТ!"}

async def send_ping():
    await asyncio.sleep(10)
    render_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')}.onrender.com"
    async with httpx.AsyncClient() as client_http:
        while True:
            if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
                try: await client_http.get(render_url)
                except: pass
            await asyncio.sleep(300)

phone_number = "+380957708743"
phone_code_hash = None

# Этот обработчик сработает ТОЛЬКО когда мы пнем его руками
@bot_client.on(events.NewMessage(pattern='/start'))
async def start(event):
    global phone_code_hash
    await event.reply("🚀 Запрос кода отправлен...")
    try:
        await user_client.connect()
        send_code_res = await user_client.send_code_request(phone_number)
        phone_code_hash = send_code_res.phone_code_hash
        await event.reply("📩 Код в телеге! Напиши его сюда цифрами.")
    except Exception as e:
        await event.reply(f"❌ Ошибка: {e}")

@bot_client.on(events.NewMessage())
async def handle_code(event):
    global phone_code_hash
    if event.text.startswith('/'): return
    if phone_code_hash:
        try:
            await user_client.sign_in(phone_number, event.text.strip(), phone_code_hash=phone_code_hash)
            await event.reply("👑 ПОБЕДА! Юзербот вошел.")
        except Exception as e:
            await event.reply(f"❌ Ошибка входа: {e}")

@app.on_event("startup")
async def on_startup():
    # ИСПРАВЛЕНО: Запускаем мост БЕЗ блокировки основного потока сервера!
    # Рендер теперь запустится моментально и выдаст статус LIVE!
    await user_client.connect()
    asyncio.create_task(bot_client.start(bot_token=BOT_TOKEN))
