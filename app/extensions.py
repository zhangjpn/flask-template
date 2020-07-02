# -*- coding:utf-8 -*-
"""初始化扩展"""

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, DOCUMENTS
from weixin import Weixin
from flask_migrate import Migrate


migrate = Migrate()
db = SQLAlchemy()
cors = CORS()
jwt = JWTManager()
photos = UploadSet('images', IMAGES)
documents = UploadSet('documents', DOCUMENTS)
wx = Weixin()
