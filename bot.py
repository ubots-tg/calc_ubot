#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, CallbackContext, Filters

from secure import BOT_TOKEN

from gg69_expeval import ExpEval

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


def inline_query(update: Update, context: CallbackContext):
    global expr_evaluator
    logger.debug("inline_query " + update.inline_query.query)
    query = update.inline_query.query
    result, success = expr_evaluator.comp_exp(query)
    query_results = []
    if expr_evaluator.is_this_code_for_sending_result(success):
        query_results.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title=f'{query} = {result}',
                input_message_content=InputTextMessageContent(f'{query} = <b>{result}</b>', parse_mode='HTML')
            )
        )
    update.inline_query.answer(query_results)


def dm_query(update: Update, context: CallbackContext):
    logger.debug("dm_query " + update.message.text)
    global expr_evaluator
    query = update.message.text
    result, success = expr_evaluator.comp_exp(query)
    if expr_evaluator.is_this_code_for_sending_result(success):
        update.message.reply_text(f'{query} = <b>{result}</b>', parse_mode='HTML')
    # else:
    #     update.message.reply_text(f'<b>Error:</b> {result}', parse_mode='HTML')


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
    dp.add_handler(InlineQueryHandler(inline_query))
    dp.add_handler(MessageHandler(Filters.text, dm_query))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    # TODO: сделать логгинг
    expr_evaluator = ExpEval()
    main()
