from loader import dp, db
from aiogram import types
from aiogram.dispatcher import FSMContext

from states.registration import Registration
from keyboards.default.default_buttons import phone_button

from utils import get_now

import re


@dp.callback_query_handler(lambda c: c.data == 'register')
async def register_callback(call: types.CallbackQuery):
    print("men shetta")
    await call.message.answer("Iltimos, ismingiz va familiyangizni kiriting:")
    await Registration.full_name.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=Registration.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    message_text = message.text
    if "/start" in message_text or len(message_text.split()) < 2 or not message_text.replace(" ", "").isalpha():
        await message.answer("Iltimos ism familiyangizni to'liq kiriting!")
        await Registration.full_name.set()
    else:
        await state.update_data(full_name=message.text)
        await message.answer("Telefon raqamingizni +998901644101 ko'rinishda kiriting yoki quyidagi tugma yordamida raqamingizni ulashing:", reply_markup=phone_button)
        await Registration.phone_number.set()


@dp.message_handler(state=Registration.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    await message.answer("Iltimos ism familiyangizni kiriting!")
    await Registration.full_name.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Registration.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    contact = message.contact
    await state.update_data(phone_number=contact.phone_number)
    await save_user_data(message, state)


@dp.message_handler(content_types=types.ContentType.TEXT, state=Registration.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    contact = message.text
    pattern = r"^\+998\d{9}$"
    if re.match(pattern, contact):
        await state.update_data(phone_number=contact)
    else:
        await message.answer("Iltimos telefon raqamingizni to'liq kiriting yoki quyidagi tugma yordamida telefon raqamingizni ulashing.", reply_markup=phone_button)
        await Registration.phone_number.set()


@dp.message_handler(state=Registration.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await message.answer("Iltimos telefon raqamingizni to'liq kiriting yoki quyidagi tugma yordamida telefon raqamingizni ulashing.", reply_markup=phone_button)
    await Registration.phone_number.set()


async def save_user_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await db.add_user(
            full_name=data.get("full_name"),
            username=message.from_user.username,
            telegram_id=message.from_user.id,
            phone_number=data.get("phone_number"),
            created_at=await get_now(),
        )
        await message.answer("Muvaffaqiyatli ro'yxatdan o'tdingiz! Botdan foydalanishingiz mumkin.")
    except:
        await message.answer("Ro'yxatdan o'tish muaffaqiyatli tugatilmadi! Iltimos qayta urinib ko'ring.")