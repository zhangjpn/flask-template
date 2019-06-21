# -*- coding:utf-8 -*-

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def success_response(payload=None, msg=None):
    res_data = {'code': 0, 'data': payload or {}}
    if msg:
        res_data['msg'] = msg
    response = jsonify(res_data)
    response.status_code = 200

    return response


def error_response(status_code, msg=None):
    """api错误处理"""
    response = jsonify({'code': status_code, 'msg': msg or HTTP_STATUS_CODES.get(status_code, 'Unknown error')})
    response.status_code = 200
    return response


def bad_request(msg):
    return error_response(400, msg)


def not_found_response(msg=None):
    return error_response(404, msg=msg or 'Resource not found')


def resource_occupied(msg=None):
    return error_response(410, msg=msg or 'Resource occupied')
