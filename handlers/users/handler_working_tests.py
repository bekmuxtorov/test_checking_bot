from aiogram import types
from loader import db, dp
from aiogram.dispatcher import FSMContext

from states.working_tests import AddTest
from keyboards.inline import make_inline_buttons, admin_inline_buttons
from utils import get_now


@dp.callback_query_handler(lambda c: c.data == 'add_test')
async def register_callback(call: types.CallbackQuery):
    await call.message.answer("📋Savollar sonini kiriting:")
    await call.message.delete()
    await AddTest.Count.set()


@dp.message_handler(state=AddTest.Count)
async def process_test_count(message: types.Message, state: FSMContext):
    test_count = message.text
    if test_count.isnumeric():
        await state.update_data(test_count=int(test_count))
        await message.answer("📝Javoblarni ketma-ketlikda kiriting. \n\n<i>Namuna: abcababbcaabccaaabbba</i>")
        await AddTest.Answers.set()
    else:
        await message.answer("📋Iltimos test savollar sonini kiriting: ")
        await AddTest.Count.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=AddTest.Answers)
async def process_answers(message: types.Message, state: FSMContext):
    answers = message.text
    data = await state.get_data()
    test_count = data.get("test_count")
    if len(answers) != test_count:
        await message.answer(
            f"‼️Iltimos test javoblarni to'liq kiriting! \n\nSavollar soni {test_count} ta, lekin kiritilgan javoblar soni {len(answers)} ta"
        )
        await AddTest.Answers.set()
    else:
        buttons = {
            "Ha": "yes",
            "Yo'q": "no"
        }
        await message.answer(
            f"📋Savollar soni: {test_count} ta\n📊Javoblar: {answers}\n👤Tuzuvchi: {message.from_user.first_name}\n\n💡Tasdiqlaysizmi?",
            reply_markup=make_inline_buttons(buttons, row_width=2)
        )
        await state.update_data(answers=answers)
        await AddTest.Confirm.set()


@dp.message_handler(state=AddTest.Count)
async def process_answers(message: types.Message, state: FSMContext):
    await message.answer("‼️Iltimos test javoblarini ketma-ketlikda kiriting.\n\n\n\n<i>Namuna: abcababbcaabccaaabbba</i>")
    await AddTest.Answers.set()


@dp.callback_query_handler(text="yes", state=AddTest.Confirm)
async def process_yes(call: types.CallbackQuery, state: FSMContext):
    print("men shetta")
    await call.message.delete()
    data = await state.get_data()
    test = await db.add_test(
        test_count=data.get("test_count"),
        answers=data.get("answers"),
        created_user=call.from_user.id,
        created_at=await get_now()
    )
    user = await db.select_user(telegram_id=test.get('created_user'))
    print(await get_now())
    await call.message.answer(
        f"📝Test kodi: <code>{test.get('id')} </code>\n📋Savollar soni: {test.get('test_count')}\n👤Tuzuvchi: {user.get('full_name')}\n📅Sana: {test.get('created_at').strftime('%d/%m/%Y')}\n📊Javoblar: {test.get('answers')}"
    )
    await call.message.answer(text="✅Test muaffaqiyatli qo'shildi!")
    await state.finish()


@dp.callback_query_handler(text="no", state=AddTest.Confirm)
async def process_no(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("‼️Bekor qilindi, qayta urinib ko'rishingiz mumkin.", reply_markup=admin_inline_buttons)
    await state.finish()
