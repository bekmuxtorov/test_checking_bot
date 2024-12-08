from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def become_member_buttons(must_member: dict):
    become_member = InlineKeyboardMarkup(row_width=1)
    for channel, title in must_member.items():
        channel_link = f'https://{channel}.t.me'
        button = InlineKeyboardButton(text=title, url=f"{channel_link}")
        become_member.insert(button)

    check_button = InlineKeyboardButton(
        text='🔔 Obuna bo\'ldim', callback_data="check_button")
    become_member.insert(check_button)
    return become_member


def make_inline_buttons(words: dict, row_width: int = 1) -> InlineKeyboardMarkup:
    buttons_group = InlineKeyboardMarkup(row_width=row_width)
    for text, callback_data in words.items():
        if text is not None and callback_data is not None:
            buttons_group.insert(InlineKeyboardButton(
                text=text, callback_data=callback_data))
    return buttons_group


register_button = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Ro'yhatdan o'tish", callback_data="register")
)

buttons = {
    "Bo'lim qo'shish": "add_departmant",
    "Test qo'shish": "add_test",
    "Natijalar": "results",
    "Foydalanuvchilar": "users"
}
admin_inline_buttons = make_inline_buttons(
    words=buttons,
    row_width=2
)

for_yesno_button = {
    "Ha": "yes",
    "Yo'q": "no"
}

yesno_button = make_inline_buttons(
    words=for_yesno_button,
    row_width=2
)

for_working_test = {
    "💡Test ishlash": "work_test"
}
working_test_button = make_inline_buttons(
    words=for_working_test,
    row_width=1
)