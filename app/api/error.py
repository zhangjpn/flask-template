# -*- coding:utf-8 -*-
from weixin.login import WeixinLoginError

from . import bp
from jsonschema import ValidationError
from .res import error_response
from flask_uploads import UploadNotAllowed
from app.exceptions import OperationNotAllowedError
import logging

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


