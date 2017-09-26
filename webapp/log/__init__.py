# encoding: utf-8

from webapp import app
from logging import FileHandler, INFO, Formatter
from config import current_config


handler = FileHandler(current_config.flask_log, encoding='UTF-8')

logging_format = Formatter(
            '%(levelname)s %(asctime)s [%(name)s:%(module)s:%(funcName)s:%(lineno)s] %(message)s')
handler.setFormatter(logging_format)
handler.setLevel(INFO)

app.logger.addHandler(handler)
