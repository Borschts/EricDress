import os
import asyncio
import logging
import random

import coloredlogs
from telepot import glance
from telepot.aio import DelegatorBot
from telepot.aio.delegate import create_open
from telepot.aio.helper import AnswererMixin, InlineUserHandler
from telepot.aio.loop import MessageLoop
from telepot.delegate import pave_event_space, per_inline_from_id

__author__ = 'smailzhu'

logging.basicConfig(level=logging.DEBUG)
coloredlogs.install(level='DEBUG')

TOKEN = os.environ.get('token', None)


class InlineHandler(InlineUserHandler, AnswererMixin):
    def __init__(self, *args, **kwargs):
        super(InlineHandler, self).__init__(*args, **kwargs)

    def on_inline_query(self, msg):
        query_id, from_id, query_string = glance(msg, flavor='inline_query')

        def compute_answer():
            tmp = open('content.txt', 'r').read()
            sayList = tmp.split(',\n')[0:-1]
            articles = [{'type': 'article', 'id': 'id', 'title': '虎虎?', 'message_text': random.choice(sayList)}]

            return articles, 0

        self.answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = glance(msg, flavor='chosen_inline_result')
        s = f"{msg['from']['first_name']}: Chosen Inline Result: {result_id} {from_id} {query_string}"
        logging.info(s)

    def on_close(self, ex):
        pass


bot = DelegatorBot(TOKEN, [
    pave_event_space()(
        per_inline_from_id(), create_open, InlineHandler, timeout=10),
])
loop = asyncio.get_event_loop()

loop.create_task(MessageLoop(bot).run_forever())
logging.info('Listening ...')

loop.run_forever()
