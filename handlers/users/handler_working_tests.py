from aiogram import types
from loader import db, dp, bot
from aiogram.dispatcher import FSMContext

from states.working_tests import AddTest, AddDepartment, WorkTest
from keyboards.default.default_buttons import make_buttons, cancel_button
from keyboards.inline import make_inline_buttons, admin_inline_buttons
from utils import get_now

# add depormant
# 1. Bo'lim nomi
# 2. Tasnif
# 3. Yaratilgan sana


@dp.callback_query_handler(lambda c: c.data == "add_departmant")
async def adding_departmant(call: types.CallbackQuery):
    await call.message.answer("➕ Bo'lim nomini kiriting:", reply_markup=cancel_button)
    await call.message.delete()
    await AddDepartment.Name.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=AddDepartment.Name)
async def process_adding_departmant(message: types.Message, state: FSMContext):
    departmant_name = message.text
    await state.update_data(departmant_name=departmant_name)
    await message.answer("📝 Bo'lim haqida qisqacha ma'lumotni kiriting:")
    await AddDepartment.Description.set()


@dp.message_handler(state=AddDepartment.Name)
async def process_adding_departmant(message: types.Message, state: FSMContext):
    await message.answer("💡 Iltimos bo'lim nomini text holatida kiriting:")
    await AddDepartment.Name.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=AddDepartment.Description)
async def process_adding_departmant(message: types.Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    name = data.get("departmant_name")
    await db.add_departmant(
        name=name,
        description=description,
        created_at=await get_now()
    )
    await message.answer("✅Muaffaqiyatli yangi bo'lim yaratildi!", reply_markup=admin_inline_buttons)
    await state.finish()


@dp.message_handler(state=AddDepartment.Name)
async def process_adding_departmant(message: types.Message, state: FSMContext):
    await message.answer("💡 Iltimos bo'lim haqida ma'lumotni text holatida kiriting:")
    await AddDepartment.Description.set()


# Add test
@dp.callback_query_handler(lambda c: c.data == 'add_test')
async def register_callback(call: types.CallbackQuery):
    await call.message.answer("📃Test fayl manzilini kiriting yoki o'tkazib yuboring:", reply_markup=make_buttons(["O'tkazib yuborish", "❌ Bekor qilish"], row_width=1))
    await call.message.delete()
    await AddTest.FileAddress.set()


@dp.message_handler(text="O'tkazib yuborish", state=AddTest.FileAddress)
async def process_test_count(message: types.Message, state: FSMContext):
    await state.update_data(file_address="")
    depts = await get_departmant()
    inline_depts_buttons = make_inline_buttons(depts, row_width=2)
    service_message = await message.answer('.', reply_markup=types.ReplyKeyboardRemove())
    await service_message.delete()
    service_message_for_cancel = await message.answer('.', reply_markup=cancel_button)
    await service_message_for_cancel.delete()
    await message.answer("📝 Test bo'limini tanglang:", reply_markup=inline_depts_buttons)
    await message.delete()
    await AddTest.Departmant.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=AddTest.FileAddress)
async def process_test_count(message: types.Message, state: FSMContext):
    file_address = message.text
    if not (file_address.startswith("http://") or file_address.startswith("https://")):
        await message.reply("Iltimos, to‘g‘ri havola yuboring.")
        await AddTest.FileAddress.set()
        return

    await state.update_data(file_address=file_address)
    depts = await get_departmant()
    inline_depts_buttons = make_inline_buttons(depts, row_width=2)
    service_message = await message.answer('.', reply_markup=types.ReplyKeyboardRemove())
    await service_message.delete()
    service_message_for_cancel = await message.answer('.', reply_markup=cancel_button)
    await service_message_for_cancel.delete()
    await message.answer("📝 Test bo'limini tanglang:", reply_markup=inline_depts_buttons)
    await AddTest.Departmant.set()


async def get_departmant():
    data = dict()
    depts = await db.select_all_departmants()
    for dept in depts:
        id = dept.get("id")
        data[dept.get("name")] = f"dept_{id}"
    print(data)
    return data


@dp.message_handler(state=AddTest.FileAddress)
async def process_test_count(message: types.Message, state: FSMContext):
    await message.answer("📝 Iltimos test fayl manzilini kiriting yoki o'tkazib yuboring:")
    await AddTest.FileAddress.set()
    await message.delete()

    # if test_count.isnumeric():
    #     await state.update_data(test_count=int(test_count))
    #     await message.answer("📝Javoblarni ketma-ketlikda kiriting. \n\n<i>Namuna: abcababbcaabccaaabbba</i>")
    #     await AddTest.Answers.set()
    # else:
    #     await message.answer("📋Iltimos test savollar sonini kiriting: ")
    #     await AddTest.Count.set()


@dp.callback_query_handler(text_contains="dept_", state=AddTest.Departmant)
async def is_member(call: types.CallbackQuery, state: FSMContext):
    message = call.data
    print(message)
    dept_id = int(message.split("_")[1])
    print(dept_id)
    await state.update_data(dept_id=dept_id)

    await call.message.answer("📋Savollar sonini kiriting:")
    await call.message.delete()
    await AddTest.Count.set()


@dp.message_handler(state=AddTest.Departmant)
async def is_member(message: types.Message, state: FSMContext):
    depts = await get_departmant()
    inline_depts_buttons = make_inline_buttons(depts, row_width=2)
    await message.answer("⚡ Quyidagilardan test uchun bo'lim tanlang:", reply_markup=inline_depts_buttons)
    await message.delete()
    service_message_for_cancel = await message.answer('.', reply_markup=cancel_button)
    await service_message_for_cancel.delete()
    await AddTest.Departmant.set()


@dp.message_handler(state=AddTest.Count)
async def process_test_count(message: types.Message, state: FSMContext):
    test_count = message.text
    if test_count.isnumeric():
        await state.update_data(test_count=int(test_count))
        await message.answer("📝Javoblarni ketma-ketlikda kiriting. \n\n<i>Namuna: abcababbcaabccaaabbba</i>")
        service_message_for_cancel = await message.answer('.', reply_markup=cancel_button)
        await service_message_for_cancel.delete()
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
        get_dept = await db.select_departmant(id=int(data.get("dept_id")))

        await message.answer(
            f"🆔Bo'lim: {get_dept.get('name')}\n📋Savollar soni: {test_count} ta\n📊Javoblar: {answers}\n👤Tuzuvchi: {message.from_user.first_name}\n\n💡Tasdiqlaysizmi?",
            reply_markup=make_inline_buttons(buttons, row_width=2)
        )
        await state.update_data(answers=answers)
        await AddTest.Confirm.set()


@dp.message_handler(state=AddTest.Count)
async def process_answers(message: types.Message, state: FSMContext):
    await message.answer("‼️Iltimos test javoblarini ketma-ketlikda kiriting.\n\n\n\n<i>Namuna: abcababbcaabccaaabbba</i>", reply_markup=cancel_button)
    await AddTest.Answers.set()


@dp.callback_query_handler(text="yes", state=AddTest.Confirm)
async def process_yes(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    test = await db.add_test(
        dept_id=data.get("dept_id"),
        file_address=data.get("file_address"),
        test_count=data.get("test_count"),
        answers=data.get("answers"),
        created_user=call.from_user.id,
        created_at=await get_now()
    )
    user = await db.select_user(telegram_id=test.get('created_user'))
    get_dept = await db.select_departmant(id=int(data.get("dept_id")))
    caption = f"📝Test kodi: <code>{test.get('id')} </code>\n🆔Bo'lim: {get_dept.get('name')}\n📋Savollar soni: {test.get('test_count')}\n👤Tuzuvchi: {user.get('full_name')}\n📅Sana: {test.get('created_at').strftime('%d/%m/%Y')}\n\n📊Javoblar: {test.get('answers')}"
    link = data.get("file_address")
    if link:
        await bot.send_document(chat_id=call.message.chat.id, document=link, caption=caption)
    else:
        await call.message.answer(text=caption)

    await call.message.answer(text="✅Test muaffaqiyatli qo'shildi!", reply_markup=admin_inline_buttons)
    await state.finish()


@dp.callback_query_handler(text="no", state=AddTest.Confirm)
async def process_no(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("‼️Bekor qilindi, qayta urinib ko'rishingiz mumkin.", reply_markup=admin_inline_buttons)
    await state.finish()


# Work test in bot
@dp.callback_query_handler(text="work_test")
async def process_no(call: types.CallbackQuery, state: FSMContext):
    depts = await get_departmant()
    # await call.message.delete()
    inline_depts_buttons = make_inline_buttons(depts, row_width=2)
    await call.message.answer("📜 Mos bo'limni tanlang:", reply_markup=inline_depts_buttons)
    await WorkTest.Department.set()


@dp.callback_query_handler(text_contains="dept_", state=WorkTest.Department)
async def is_member(call: types.CallbackQuery, state: FSMContext):
    message = call.data
    await call.message.delete()
    dept_id = int(message.split("_")[1])
    get_dept = await db.select_departmant(id=dept_id)
    dept_name = get_dept.get("name")
    tests_from_base = await db.select_tests_from_dept(dept_id=dept_id)
    depts = await get_departmant()
    # await call.message.delete()
    inline_depts_buttons = make_inline_buttons(depts, row_width=2)

    tests = dict()
    if not tests_from_base:
        await call.message.answer(
            text="Ushbu bo'limga testlar joylanmagan, boshqa bo'limni tanlashingiz mumkin",
            reply_markup=inline_depts_buttons
        )
        await WorkTest.Department.set()
        return

    for test in tests_from_base:
        status = await db.get_result_by_user(telegram_id=call.message.chat.id, test_id=int(test.get("id")))
        if status:
            tests[f"{test.get('id')} ✅"] = f"test_{test.get('id')}"
        else:
            tests[f"{test.get('id')}"] = f"test_{test.get('id')}"

    test_inline_buttons = make_inline_buttons(words=tests, row_width=3)
    await call.message.answer(f"💡 Yaxshi!\n\n{dept_name} bo'limidagi testlar quyida ko'rinishingiz mumkin, agar bu testni avval ishlagan bo'lsangiz ✅ belgisi bilan ko'rinadi. Kerakli test tanlang:", reply_markup=test_inline_buttons)
    await state.update_data(dept_id=dept_id)
    await WorkTest.Choice.set()


@dp.message_handler(state=WorkTest.Department)
async def is_member(message: types.Message, state: FSMContext):
    depts = await get_departmant()
    await message.delete()
    inline_depts_buttons = make_inline_buttons(depts, row_width=2)
    await message.answer("Iltimos quyidagi tugmalar yordamida kerakli bo'limni tanglang:", reply_markup=inline_depts_buttons)
    await WorkTest.Department.set()


@dp.callback_query_handler(text_contains="test_", state=WorkTest.Choice)
async def is_member(call: types.CallbackQuery, state: FSMContext):
    message = call.data
    await call.message.delete()
    test_id = int(message.split("_")[1])
    test = await db.select_test(id=test_id)

    user = await db.select_user(telegram_id=test.get('created_user'))
    get_dept = await db.select_departmant(id=int(test.get("dept_id")))
    caption = f"📝Test kodi: <code>{test.get('id')} </code>\n🆔Bo'lim: {get_dept.get('name')}\n📋Savollar soni: {test.get('test_count')}\n👤Tuzuvchi: {user.get('full_name')}\n📅Sana: {test.get('created_at').strftime('%d/%m/%Y')}\n\n❗️Testga javob berish\n\n✅Test kodini kiritib # (panjara) belgisini qo'yasiz va barcha kalitlarni kiritasiz.\n\n<i>✍️Misol uchun:\ntestkodi#[javoblar ketma ketlikda]\n\n1. {test.get('id')}#abcdabcdddabaca\n2. {test.get('id')}#ABCABBCCADCABAB\n3. {test.get('id')}#123412341234324\n3. {test.get('id')}#12CD12341234ab4</i>\n\n✅Katta(A) va kichik(a) harflar bir xil hisoblanadi.\n\n👉 @newsatdigital"
    link = test.get("file_address")
    if link:
        await bot.send_document(chat_id=call.message.chat.id, document=link, caption=caption)
    else:
        await call.message.answer(text=caption)
