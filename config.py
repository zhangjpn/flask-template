# -*-coding:utf-8 -*-

import os
from datetime import timedelta, timezone
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


base_dir = os.path.dirname(__file__)


class Config(object):
    # 密钥
    HOST = os.environ.get('HOST')  # 公网域名
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'something you never gusess....'

    # 数据库连接
    SQLALCHEMY_ECHO = True  # 打印sql
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+pymysql://root:root@localhost:3306/dbname?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BROKER_URL = os.getenv('BROKER_URL',
                           'redis://localhost:6379/0')
    CELERY_ACKS_ON_FAILURE_OR_TIMEOUT = False
    CELERY_ACKS_LATE = True

    # 分页设置
    PER_PAGE = 10
    # token 过期时间
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=10)
    # secret key
    JWT_SECRET_KEY = 'some thing you never guess'
    TIME_ZONE = timezone(timedelta(hours=8))
    JWT_HEADER_TYPE = ''
    JWT_HEADER_NAME = 'Authorization'

    UPLOADS_DEFAULT_DEST = os.environ.get('UPLOADS_DEFAULT_DEST') or os.path.join(base_dir, 'uploads')  # 默认文件上传路径
    # MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # 文件上传最大大小

    UPLOADS_DEFAULT_URL = '/api/upload'

    # ====== 微信支付 ======
    WEIXIN_APP_SECRET = ''  # 小程序APP密钥
    WEIXIN_APP_ID = ''  # 小程序APP_ID
    WEIXIN_MCH_ID = ''  # 商户ID
    WEIXIN_MCH_KEY = ''  # 商户密钥
    WEIXIN_NOTIFY_URL = ''  # 支付成功通知回调URL
    WEIXIN_MCH_KEY_FILE = ''  # 商户密钥pkcs12文件  退款用到
    # more detail see https://github.com/zwczou/weixin-python
    # =====================


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/dbname?charset=utf8mb4'

    pass


class TestingConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    pass


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    pass


config = {
    'production': ProdConfig,
    'development': DevConfig,
    'testing': TestingConfig,
    'default': DevConfig,
}
