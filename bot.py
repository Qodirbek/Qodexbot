from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from fastapi import FastAPI
import asyncio
import logging
import os

TOKEN = "8064942614:AAGT-8nE_MmK45WAdv7VCChaK8jo8O1lNzU"
WEB_APP_URL = "https://qodex-game.onrender.com"
COMMUNITY_URL = "https://t.me/QODEX_COIN"
WEBHOOK_URL = "https://qodexbot.onrender.com/webhook"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
app = FastAPI()

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    if message.text == "/start":
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎮 Play Game", web_app=WebAppInfo(url=WEB_APP_URL))],
            [InlineKeyboardButton(text="📢 Join Community", url=COMMUNITY_URL)]
        ])
        start_text = "👋 QODEX COIN'ga xush kelibsiz!\n\n💰 Tugmalarni bosib tanga ishlang.\n🎮 O‘yin ichida energiya va yangilanishlar bor.\n🔗 Do‘stlaringizni taklif qilib, bonus oling!"
        await message.answer(start_text, reply_markup=keyboard)

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("🤖 Webhook o‘rnatildi!")

@app.post("/webhook")
async def webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot, telegram_update)
    return {"ok": True}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))