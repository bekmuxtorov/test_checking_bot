import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from data.config import ADMINS

from keyboards.inline.inline_buttons import register_button, admin_inline_buttons, make_inline_buttons, working_test_button
from keyboards.default.default_buttons import cancel_button


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
        print(message.from_user.id)
        if str(message.from_user.id) in ADMINS:
            await message.answer(
                text="Siz bot adminisiz, kerakli bo'limni tanlang:",
                reply_markup=admin_inline_buttons
            )
        else:
            await message.answer(
                "❗️Testga javob berish\n\n✅Test kodini kiritib # (panjara) belgisini qo'yasiz va barcha kalitlarni kiritasiz.\n\n<i>✍️Misol uchun:\ntestkodi#{javoblar ketma ketlikda}\n\n1. 47#abcdabcdddabaca\n2. 47#ABCABBCCADCABAB\n3. 47#123412341234324\n3. 47#12CD12341234ab4</i>\n\n✅Katta(A) va kichik(a) harflar bir xil hisoblanadi.")
            await message.answer(text="Quyidagi tugma yordamida test ishlashingiz ham mumkin", reply_markup=working_test_button)
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
        await call.message.answer("❗️Testga javob berish\n\n✅Test kodini kiritib # (panjara) belgisini qo'yasiz va barcha kalitlarni kiritasiz.\n\n<i>✍️Misol uchun:\ntestkodi#{javoblar ketma ketlikda}\n\n1. 47#abcdabcdddabaca\n2. 47#ABCABBCCADCABAB\n3. 47#123412341234324\n3. 47#12CD12341234ab4</i>\n\n✅Katta(A) va kichik(a) harflar bir xil hisoblanadi.")
        await call.message.answer(text="Quyidagi tugma yordamida test ishlashingiz ham mumkin", reply_markup=working_test_button)
    else:
        await call.message.answer(
            text="Assalomu alaykum ustoz!\n\nTest tekshiruvchi botga xush kelibsiz!\nQuyidagi tugma yordamida botdan ro'yhatdan o'ting va botning barcha imkoniyatlaridan bepulga foydalaning.",
            reply_markup=register_button
        )


@dp.callback_query_handler(lambda c: c.data == "results")
@dp.callback_query_handler(lambda c: c.data == "users")
async def adding_departmant(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("🛠️ Bu bo'lim ishlab chiqish jarayonida...")
    await state.finish()


@dp.message_handler(text="❌ Bekor qilish", state="*")
async def send_ad_to_all(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text="⚡ Jarayon bekor qilindi!"
    )
    service_message_for_cancel = await message.answer('.', reply_markup=cancel_button)
    await service_message_for_cancel.delete()
    if str(message.from_user.id) in ADMINS:
        await message.answer(
            text="Siz bot adminisiz, kerakli bo'limni tanlang:",
            reply_markup=admin_inline_buttons
        )
    else:
        await message.answer(
            "❗️Testga javob berish\n\n✅Test kodini kiritib # (panjara) belgisini qo'yasiz va barcha kalitlarni kiritasiz.\n\n<i>✍️Misol uchun:\ntestkodi#{javoblar ketma ketlikda}\n\n1. 47#abcdabcdddabaca\n2. 47#ABCABBCCADCABAB\n3. 47#123412341234324\n3. 47#12CD12341234ab4</i>\n\n✅Katta(A) va kichik(a) harflar bir xil hisoblanadi.")
        await message.answer(text="Quyidagi tugma yordamida test ishlashingiz ham mumkin", reply_markup=working_test_button)
