# -*-coding:utf-8 -*-

import os
import logging
from dotenv import load_dotenv
from app import create_app

# 需先加载环境变量

dot_env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dot_env_path):
    load_dotenv(dot_env_path)

from config import ProdConfig

app = create_app(ProdConfig)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.setLevel(gunicorn_logger.level)
