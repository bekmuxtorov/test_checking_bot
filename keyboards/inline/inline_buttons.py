from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

register_button = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Ro'yhatdan o'tish", callback_data="register")
)
