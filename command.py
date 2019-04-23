import re
import sys
import time
import random
import logging

import redis
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
        self.client = redis.from_url(self.config.get('redis', 'url'))

    @run_async
    def update_dict(self, bot, update):
        url = self.config.get('content', 'url')
        r = requests.get(url)
        if r.status_code != 200:
            return
        self.client.delete('dress')
        for world in r.text.split(',\n'):
            if world:
                self.client.lpush('dress', world)
        if update.message:
            update.message.reply_text('Updated.')

    @run_async
    def dong(self, bot, update):
        query = update.inline_query.query
        if self.client.lindex('dress', 0) == None:
            self.update_dict(bot, update).result()
        total = self.client.llen('dress')
        seed = self.client.lindex('dress', random.randint(0, total-1))

        results = [InlineQueryResultArticle(
            id=update.inline_query.id,
            title='虎虎？',
            thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/198/dress_1f457.png',
            input_message_content=InputTextMessageContent(seed.decode()))]
        bot.answer_inline_query(update.inline_query.id, results, cache_time=0)

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)
