from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
