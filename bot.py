#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from uuid import uuid4
import sys

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, CallbackContext, Filters
import numexpr
from secure import BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Привет! Я могу посчитать, например, вот это:\n'
        '`2 + 4 * 5`\n'
        '`12 / 3`\n'
        '`sqrt(4)`\n'
        'Просто напишите мне любой пример!\n',
        parse_mode='Markdown'
    )


def inlinequery(update: Update, context: CallbackContext):
    query = update.inline_query.query
    try:
        result = numexpr.evaluate(query).item()
        query_results = [InlineQueryResultArticle(
            id=uuid4(),
            title=result,
            description=f'{query} = {result}',
            input_message_content=InputTextMessageContent(f'{query} = <b>{result}</b>', reply_markup='HTML')
        )]
    except Exception as e:
        # exc_type, exc_value, exc_traceback = sys.exc_info()
        # result = f'{exc_type.__name__}: {str(exc_value)}'
        # result = 'Error!'
        query_results = []
        diff_count = query.count('(') - query.count(')')
        if diff_count > 0:
            query += ')' * diff_count
            try:
                result = numexpr.evaluate(query).item
                query_results = [InlineQueryResultArticle(
                                 id=uuid4(),
                                 title=result,
                                 input_message_content=InputTextMessageContent(f'{query} = <b>{result}</b>', parse_mode='HTML')
                                )]
            except Exception:
                query_results = []

    update.inline_query.answer(query_results)


def dmquery(update: Update, context: CallbackContext):
    query = update.message.text
    try:
        result = numexpr.evaluate(query).item()
        update.message.reply_text(f'{query} = <b>{result}</b>', parse_mode='HTML')
    except Exception as e:
        update.message.reply_text('Error')


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
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(MessageHandler(Filters.text, dmquery))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
