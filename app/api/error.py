# -*- coding:utf-8 -*-

import logging

from jsonschema import ValidationError
from weixin.login import WeixinLoginError
from flask import jsonify

from flask_uploads import UploadNotAllowed
from app.exceptions import OperationNotAllowedError
from app.extensions import jwt
from app.models.user import User

from .res import error_response
from . import bp


@bp.errorhandler(400)
@bp.errorhandler(UploadNotAllowed)
@bp.errorhandler(ValidationError)
def invalid_parameter_error(e):
    return error_response(400, msg=e.args[0] if len(e.args) > 0 else 'Invalid parameter')


@bp.errorhandler(401)
def invalid_authorizaion(e):
    if len(e.args) > 0:
        msg = e.args[0]
        print(msg)
    else:
        msg = 'Unauthorized'
    return error_response(401, msg=msg)


@bp.errorhandler(OperationNotAllowedError)
def operation_not_allowed(e):
    if len(e.args) > 0:
        msg = e.args[0]
    else:
        msg = 'Operation not allowed'
    return error_response(403, msg=msg)


@bp.errorhandler(WeixinLoginError)
def wx_login_error_handler(e):
    """微信登陆错误处理器"""
    logging.exception(e)
    return error_response(500, msg='Weixin login service not available')


@jwt.expired_token_loader
def expired_token_callback(e):
    """过期操作"""
    return jsonify({'code': 401, 'err_msg': 'Token has expired '})


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
