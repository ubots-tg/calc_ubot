#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from uuid import uuid4
import sys

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
import numexpr
from secure import BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi!')


def inlinequery(update: Update, context: CallbackContext):
    query = update.inline_query.query
    print(query)
    try:
        result = numexpr.evaluate(query).item()
    except Exception as e:
        # exc_type, exc_value, exc_traceback = sys.exc_info()
        # result = f'{exc_type.__name__}: {str(exc_value)}'
        result = 'Error!'
    query_results = [InlineQueryResultArticle(
        id=uuid4(),
        title=result,
        input_message_content=InputTextMessageContent(f'{query} = {result}'), )]

    update.inline_query.answer(query_results)


def error(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(BOT_TOKEN, use_context=True, request_kwargs={
        'proxy_url': 'socks5h://t.geekclass.ru:7777',
        'urllib3_proxy_kwargs': {
            'username': 'geek',
            'password': 'socks',
        }
    })

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(InlineQueryHandler(inlinequery))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
