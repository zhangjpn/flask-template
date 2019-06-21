# -*-coding:utf-8 -*-

from app import create_app
import logging
app = create_app('production')

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.setLevel(gunicorn_logger.level)
