import logging
import coloredlogs
import random
import requests
from telepot import glance
from telepot.aio.helper import AnswererMixin, InlineUserHandler

__author__ = 'smailzhu'

logging.basicConfig(level=logging.DEBUG)
coloredlogs.install(level='DEBUG')


class InlineHandler(InlineUserHandler, AnswererMixin):
    def __init__(self, *args, **kwargs):
        super(InlineHandler, self).__init__(*args, **kwargs)

    def on_inline_query(self, msg):
        query_id, from_id, query_string = glance(msg, flavor='inline_query')

        def compute_answer():
            try:
                content_link = "https://raw.githubusercontent.com/hexUniverse/postergirl/master/content.txt"
                tmp = requests.get(content_link).text
            except Exception as e:
                tmp = open('content.txt', 'r', encoding='utf8').read()
                logging.WARN(e)
            random.seed(query_string)
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
