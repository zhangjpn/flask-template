# -*- coding:utf-8 -*-
"""
"""
from datetime import datetime, timedelta

from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from jsonschema import validate

from app.api.res import success_response
from app.extensions import wx, db
from app.models.user import User
from . import bp


@bp.route('/c/login', methods=('POST',))
def client_login():
    """小程序登陆"""
    body = request.get_json()
    validate(body, {
        'properties': {
            'code': {
                'type': 'string',
            }
        },
        'required': ['code'],
        'type': 'object',
    })
    code = body.get('code')
    # {'openid': openid, 'session_key': session_key, 'unionid': unionid, errcode:{}}
    session_info = wx.login.jscode2session(code)
    # 信息写入
    open_id = session_info.get('openid')
    union_id = session_info.get('unionid')
    session_key = session_info.get('session_key')

    user = User.query.filter_by(app_id=wx.app_id, open_id=open_id).first()
    if not user:
        user = User.create_from_wx(open_id=open_id, session_key=session_key, union_id=union_id, app_id=wx.app_id, )
    else:
        user.session_key = session_key

    db.session.add(user)
    db.session.commit()
    expire_time = timedelta(days=30)
    expire_at = (datetime.now() + expire_time).timestamp()
    token = create_access_token({'user_id': user.id}, expires_delta=expire_time)

    return success_response({'access_token': token, 'expire_at': expire_at})


@bp.route('/c/userinfo/save', methods=('POST',))
# @jwt_required
def get_client_user_info():
    """保存用户信息"""
    body = request.get_json()
    validate(body, {
        'properties': {
            'userInfo': {
                'type': 'object',
            }
        },
        'type': 'object',
    })

    # signature 是使用iv对userInfo的加密签名，用来防止传输过程信息被篡改
    #
    return success_response({})
