from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import CHANNELS
from utils.check_in_channel import check
from loader import bot

from keyboards.inline import become_member_buttons


class Asosiy_checking(BaseMiddleware):
    async def on_pre_process_update(self, xabar: types.Update, data: dict):
        status_message = False
        if xabar.message:
            user_id = xabar.message.from_user.id
            chat_type = xabar.message.chat.type
        elif xabar.callback_query:
            user_id = xabar.callback_query.from_user.id
            chat_id = xabar.callback_query.message.chat.id
            status_message = True
            chat_type = xabar.callback_query.message.chat.type
        else:
            return

        if chat_type == types.ChatType.PRIVATE:
            dastlabki_holat = True
            must_member = {}
            hello_text = "Assalomu alekum, botga xush kelibsiz"
            for channel in CHANNELS:
                holat = await check(user_id=user_id, channel=channel)
                dastlabki_holat *= holat
                channel = await bot.get_chat(channel)
                if not holat:
                    link = channel.username
                    must_member[link] = channel.title
            if not dastlabki_holat:
                first_text = f"📤 {hello_text}.\n\nFoydalanish uchun quyidagi kanallarga a'zo bo'lishingiz kerak!"

                if status_message:
                    first_text = f"📤Foydalanish uchun kanallarning barchasiga a'zo bo'lishingiz kerak!"
                    await bot.send_message(chat_id, first_text, reply_markup=become_member_buttons(must_member))
                else:
                    await xabar.message.reply(first_text, reply_markup=become_member_buttons(must_member))
                raise CancelHandler()
