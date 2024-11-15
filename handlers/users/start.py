import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import ADMINS

from keyboards.inline.inline_buttons import register_button


# @dp.message_handler(CommandStart())
# async def bot_start(message: types.Message):
#     # try:
#     #     user = await db.add_user(telegram_id=message.from_user.id,
#     #                              full_name=message.from_user.full_name,
#     #                              username=message.from_user.username)
#     # except asyncpg.exceptions.UniqueViolationError:
#     #     user = await db.select_user(telegram_id=message.from_user.id)

#     await message.answer("Xush kelibsiz!")

#     # ADMINGA xabar beramiz
#     count = await db.count_users()
#     msg = f"{user[1]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
#     await bot.send_message(chat_id=ADMINS[0], text=msg)

@dp.message_handler(CommandStart(),  state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()

    user = await db.select_user(telegram_id=message.from_user.id)
    if user:
        await message.answer(
            "Siz ro'yhatdan o'tgansiz, botdan foydalanishingiz mumkin!")
    else:
        await message.answer(
            text="Assalomu alaykum ustoz!\n\nTest tekshiruvchi botga xush kelibsiz!\nQuyidagi tugma yordamida botdan ro'yhatdan o'ting va botning barcha imkoniyatlaridan bepulga foydalaning.",
            reply_markup=register_button
        )
