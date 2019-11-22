#!/usr/bin/env python
import logging
from uuid import uuid4

from telegram import (
    Bot, ParseMode, InlineQueryResultArticle, InputTextMessageContent
)

from recycle_bot import settings
from recycle_bot.utils import to_tg_update, predict_key


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)

bot = Bot(settings.TOKEN)


def notify_admin(text, admin_uid=settings.ADMIN_UID, parse_mode=ParseMode.HTML):
    bot.send_message(
        admin_uid,
        text,
        disable_web_page_preview=True,
        parse_mode=parse_mode,
    )


def inline_search(update, datum):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(), title=x,
            input_message_content=InputTextMessageContent(
                datum.get_info(x), parse_mode=ParseMode.HTML))
        for x in datum.get_sub_keys(query.lower())
    ]
    return update.inline_query.answer(results)


@to_tg_update(bot)
def process_message(update, datum):
    if update.inline_query:
        print('inline_search ' + str(update.inline_query))
        return inline_search(update, datum)

    if not update.message:
        return

    text = update.message.text
    user_chat_id = update.message.chat.id

    if text == '/start':
        print('Greeting new user ' + str(user_chat_id))
        bot.send_message(
            user_chat_id,
            'Добро пожаловать',
        )
        result = f'New user {user_chat_id}'

    else:
        result = datum.get_info(text)
        if result:
            bot.send_message(
                user_chat_id,
                result,
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )
        else:
            keys = predict_key(text, datum.keys(), words=3)
            result = 'Возможно вы имели ввиду: ' + ', '.join(keys)
            bot.send_message(
                user_chat_id,
                result,
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML,
            )

    if user_chat_id != settings.ADMIN_UID:
        user = update.message.from_user

        notify_admin(
            f'{user_chat_id} @{user.name} {user.username} {user.first_name} {user.last_name}: {text}\n{result}')
