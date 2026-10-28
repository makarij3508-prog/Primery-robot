import asyncio
import logging
import os
import uvicorn
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from fastapi import FastAPI
import httpx

# ================= НАСТРОЙКИ =================
# Твой новый рабочий токен бота
BOT_TOKEN = "9202692783:AAHyqJXy3SpcoW7hteWfHWAreS1Tb-EoGjY"
RENDER_URL = "https://onrender.com"  # URL обновится после перезапуска Render
# =============================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Бот активен, автопинг работает!"}

async def send_ping():
    await asyncio.sleep(10)
    async with httpx.AsyncClient() as client:
        while True:
            if "onrender.com" in RENDER_URL:
                try:
                    response = await client.get(RENDER_URL)
                    logging.info(f"📟 Автопинг отправлен. Статус: {response.status_code}")
                except Exception as e:
                    logging.error(f"❌ Ошибка автопинга: {e}")
            await asyncio.sleep(300)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 **Привет! Я твой новый крипто-бот.**\n\n"
        "Я запущен на сервере Render и беру данные напрямую с Binance.\n"
        "Жми команды ниже:\n"
        "📊 /btc — Курс Bitcoin\n"
        "📊 /eth — Курс Ethereum\n"
        "📊 /ton — Курс Toncoin"
    )

async def get_price(coin: str):
    url = f"https://binance.com{coin}USDT"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            data = response.json()
            price = data['price']
            return round(float(price), 2)
        except Exception as e:
            logging.error(f"Ошибка получения курса {coin}: {e}")
            return None

@dp.message(Command("btc"))
async def btc_price(message: types.Message):
    price = await get_price("BTC")
    if price: await message.answer(f"₿ **Bitcoin (BTC):** ${price:,}")
    else: await message.answer("⚠️ Не удалось получить курс.")

@dp.message(Command("eth"))
async def eth_price(message: types.Message):
    price = await get_price("ETH")
    if price: await message.answer(f"🔷 **Ethereum (ETH):** ${price:,}")
    else: await message.answer("⚠️ Не удалось получить курс.")

@dp.message(Command("ton"))
async def ton_price(message: types.Message):
    price = await get_price("TON")
    if price: await message.answer(f"💎 **Toncoin (TON):** ${price}")
    else: await message.answer("⚠️ Не удалось получить курс.")

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(dp.start_polling(bot))
    asyncio.create_task(send_ping())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
