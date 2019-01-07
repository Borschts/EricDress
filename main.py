import os
import asyncio
import logging
import coloredlogs

from telepot.aio import DelegatorBot
from telepot.aio.delegate import create_open
from telepot.aio.loop import MessageLoop
from telepot.delegate import pave_event_space, per_inline_from_id

from inlineHandler import InlineHandler

__author__ = 'smailzhu'

logging.basicConfig(level=logging.INFO)
coloredlogs.install(level='INFO')

TOKEN = os.environ.get('token', None)


bot = DelegatorBot(TOKEN, [
    pave_event_space()(
        per_inline_from_id(), create_open, InlineHandler, timeout=10),
])
loop = asyncio.get_event_loop()

loop.create_task(MessageLoop(bot).run_forever())
logging.info('Listening ...')

loop.run_forever()
