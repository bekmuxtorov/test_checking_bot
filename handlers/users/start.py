import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import ADMINS

from keyboards.inline.inline_buttons import register_button, admin_inline_buttons


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
        if message.from_user.id in ADMINS:
            await message.answer(
                text="Siz bot adminisiz, kerakli bo'limni tanlang:",
                reply_markup=admin_inline_buttons
            )
        else:
            await message.answer(
                "❗️Testga javob berish\n\n✅Test kodini kiritib # (panjara) belgisini qo'yasiz va barcha kalitlarni kiritasiz.\n\n<i>✍️Misol uchun:\ntestkodi#{javoblar ketma ketlikda}\n\n1. 47#abcdabcdddabaca\n2. 47#ABCABBCCADCABAB\n3. 47#123412341234324\n3. 47#12CD12341234ab4</i>\n\n✅Katta(A) va kichik(a) harflar bir xil hisoblanadi.")
    else:
        await message.answer(
            text="Assalomu alaykum ustoz!\n\nTest tekshiruvchi botga xush kelibsiz!\nQuyidagi tugma yordamida botdan ro'yhatdan o'ting va botning barcha imkoniyatlaridan bepulga foydalaning.",
            reply_markup=register_button
        )


@dp.callback_query_handler(text_contains="check_button")
async def is_member(call: types.CallbackQuery,):
    user_id = call.from_user.id
    await call.message.delete()
    if call.message.chat.type in (types.ChatType.SUPERGROUP, types.ChatType.GROUP):
        await call.message.answer("💡 Guruhdan foydalanishingiz mumkin!")
        return
    user = await db.select_user(telegram_id=user_id)
    if user:
        await call.message.answer(
            "Javoblarni namuna bo'yicha jo'natishingiz mumkin: \n\n<i>Namuna:\ntestkodi#{javoblar ketma ketlikda}\n\n1. 47#abcdabcdddabaca\n2. 47#ABCABBCCADCABAB\n3. 47#123412341234324\n3. 47#12CD12341234ab4</i>")
    else:
        await call.message.answer(
            text="Assalomu alaykum ustoz!\n\nTest tekshiruvchi botga xush kelibsiz!\nQuyidagi tugma yordamida botdan ro'yhatdan o'ting va botning barcha imkoniyatlaridan bepulga foydalaning.",
            reply_markup=register_button
        )
