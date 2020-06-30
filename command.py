import re
import sys
import time
import random
import logging

import requests

import telegram
from telegram import InputTextMessageContent, InlineQueryResultArticle
from telegram.ext.dispatcher import run_async
from telegram.error import *


class app:
    '''
    db rule

    hexlightning.chat_action.json
    '''

    def __init__(self, inherit):
        logger = logging.getLogger(__name__)
        self.logger = inherit.logger
        self.config = inherit.config
        self.dress = list()

    @run_async
    def update_dict(self, bot, update):
        url = self.config.get('content', 'url')
        r = requests.get(url)
        if r.status_code != 200:
            return
        for world in r.text.split(',\n'):
            if world:
                self.dress.append(world)
        if update.message:
            update.message.reply_text('Updated.')

    @run_async
    def dong(self, bot, update):
        query = update.inline_query.query
        if self.dress == []:
            self.update_dict(bot, update).result()
        seed = random.choice(self.dress)

        results = [InlineQueryResultArticle(
            id=update.inline_query.id,
            title='劉醬？',
            thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/198/dress_1f457.png',
            input_message_content=InputTextMessageContent(seed))]
        bot.answer_inline_query(update.inline_query.id, results, cache_time=0)

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)
