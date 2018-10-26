import asyncio
import logging
import random
from configparser import ConfigParser

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

config = ConfigParser()
config.read('config.ini')
TOKEN = config.get('bot', 'token')


class InlineHandler(InlineUserHandler, AnswererMixin):
    def __init__(self, *args, **kwargs):
        super(InlineHandler, self).__init__(*args, **kwargs)

    def on_inline_query(self, msg):
        query_id, from_id, query_string = glance(msg, flavor='inline_query')

        def compute_answer():
            # print(self.id, ':', 'Inline Query:', query_id, from_id, query_string)

            sayList = ['虎虎女裝', '什麼時候要女裝啊 @allen0099', '虎虎！！！！！！', '該女裝囉虎虎',
                       '乖 穿上。', '妳再不穿上就要被濫了', '請女裝以解鎖說話權限。', '穿女裝得永生', '虎虎女裝拯救世界',
                       '虎虎女裝讓我的世界變彩色']
            articles = [{'type': 'article',
                         'id': 'id', 'title': '虎虎?', 'message_text': random.choice(sayList)}]

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
