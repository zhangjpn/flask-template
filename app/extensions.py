# -*- coding:utf-8 -*-
"""初始化扩展"""
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, DOCUMENTS
from weixin import Weixin

db = SQLAlchemy()

cors = CORS()

jwt = JWTManager()

photos = UploadSet('images', IMAGES)
documents = UploadSet('documents', DOCUMENTS)
wx = Weixin()


@jwt.expired_token_loader
def expired_token_callback(e):
    """过期操作"""
    return jsonify({'code': 401, 'err_msg': 'Token has expired '})


from app.models.user import User


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    """加载登陆用户"""
    user_id = identity.get('id')
    if not user_id:
        return None
    user = User.query.get(user_id)
    if not user:
        return None
    return user


@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    """用户未找到响应"""
    return jsonify({'code': 404, 'err_msg': 'User {} not found'.format(identity.get('id'))})
