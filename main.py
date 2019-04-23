import sys
import logging

from termcolor import *
from pprint import pprint as pp
from configparser import ConfigParser

from telegram import user
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Custom
import handle


class app:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.txt', encoding='utf8')
        self.loggingFormat = f'{colored("%(asctime)s", "white")} - {colored("%(levelname)s", "red")} - %(message)s'
        file_handler = logging.FileHandler(filename='hexlightning.log')
        stdout_handler = logging.StreamHandler(sys.stdout)
        logging_handler = [file_handler, stdout_handler]
        logging.basicConfig(
            level=logging.INFO,
            format=self.loggingFormat,
            handlers=logging_handler
        )
        self.logger = logging.getLogger(__name__)
        self.loggingFormat = f'{colored("%(asctime)s", "white")} - !name - {colored("%(levelname)s", "red")} - %(message)s'

    def run(self):
        handle.worker(
            inherit=self,
            token=self.config.get('bot', 'token'),
        )


if __name__ == '__main__':
    app = app()
    app.run()
