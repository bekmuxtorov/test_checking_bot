from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from keyboards.inline import yesno_button, working_test_button
from states.working_tests import CheckTest
from utils import get_now


@dp.message_handler(state=None)
async def process_checking_test(message: types.Message, state: FSMContext):
    answers = message.text
    if not '#' in answers:
        return

    answers_part = answers.split('#')
    if answers_part[0].isnumeric():
        test_code = int(answers_part[0])
        user_answers = answers_part[1]

        test = await db.select_test(id=test_code)
        if not test:
            await message.answer("‼️Mavjud bo'lmagan test kodi kiritildi, iltimos tekshirib qayta urinib ko'ring!")
            await state.finish()
            return

        test_count = test.get("test_count")
        answers = test.get("answers")

        if test_count != len(user_answers):
            await message.answer(
                text=f"‼️Javoblar to'liq kiritilmadi, savollar soni {test_count} ta, to'ldirib qayta yuboring!"
            )
            return

        answers_text = await view_test_with_number(test_code, user_answers)
        await message.answer(answers_text, reply_markup=yesno_button)
        await state.update_data(test_code=test_code)
        await state.update_data(user_answers=user_answers)
        await state.update_data(answers=answers)
        await CheckTest.Config.set()


@dp.callback_query_handler(text="yes", state=CheckTest.Config)
async def process_yes(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    status_answer = await checking_test(
        test_code=data.get("test_code"),
        user_answers=data.get("user_answers"),
        answers=data.get("answers")
    )
    view_test_text = await view_test_with_number(
        test_code=data.get("test_code"),
        user_answers=data.get("user_answers"),
        status_answer=status_answer
    )
    await call.message.answer(view_test_text, reply_markup=working_test_button)
    result = await db.add_result(
        test=data.get("test_code"),
        telegram_user=call.from_user.id,
        user_answers=data.get("user_answers"),
        true_count=sum(1 for value in status_answer.values() if value == "✅"),
        created_at=await get_now()
    )
    await state.finish()


@dp.callback_query_handler(text="no", state=CheckTest.Config)
async def process_yes(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("⚡️Yaxshi, kerakli paytda xizmatingizdaman!")
    await state.finish()


async def checking_test(test_code: int, user_answers: str, answers: str):
    status_answer = dict()
    for i in range(len(user_answers)):
        status_answer[f"{i+1}"] = ("✅" if answers[i]
                                   == user_answers[i] else "❌")
    return status_answer


async def view_test_with_number(test_code: int, user_answers: str, status_answer: dict = None):
    message = ''

    message += f"📝Test kodi: <code>{test_code}</code>\n"
    count = len(user_answers)
    half_count = int(count/2)
    if not status_answer:
        for i in range(half_count):
            message += f"\n{i+1}. {user_answers[i]}         {half_count+i+1}. {user_answers[half_count+i]}"
        if half_count*2 != count:
            message += f"\n{count}. {user_answers[count-1]}"
        message += "\n\n💡Tasdiqlaysizmi?"
        return message
    else:
        test = await db.select_test(id=test_code)
        user = await db.select_user(telegram_id=test.get('created_user'))
        departmant = await db.select_departmant(id=int(test.get('dept_id')))
        true_count = sum(1 for value in status_answer.values() if value == "✅")
        persent_true_count = round(
            true_count*100/int(test.get('test_count')), 2)
        message += f"👤Tuzuvchi: {user.get('full_name')}\n"
        message += f"📜Bo'lim: {departmant.get('name')} ta\n\n"
        message += f"📋Savollar soni: {test.get('test_count')} ta\n\n"
        message += f"📊To'g'ri javoblar soni: {true_count} ({persent_true_count}%)\n"
        message += f"🧮Noto'g'ri javoblar soni: {count-true_count} ({round(100-persent_true_count, 2)}%)\n"

        for i in range(half_count):
            message += f"\n{i+1}. {user_answers[i]} {status_answer.get(f'{i+1}')}         {half_count+i+1}. {user_answers[half_count+i]} {status_answer.get(f'{half_count+i+1}')}"
        if half_count*2 != count:
            message += f"\n{count}. {user_answers[count-1]} {status_answer.get(f'{count-1}')}"
        return message
