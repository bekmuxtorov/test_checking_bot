import asyncio

from aiogram import types

from data.config import ADMINS
from keyboards.inline import admin_inline_buttons
from loader import dp, db, bot


@dp.message_handler(text="/admin", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    await message.answer(
        text="Siz bot administatorisiz, kerakli bo'limni tanlang:",
        reply_markup=admin_inline_buttons
    )
