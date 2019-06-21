# -*- coding:utf-8 -*-
"""文件处理接口"""

from . import bp
from app.extensions import photos
from flask import request, jsonify, send_from_directory, current_app
import os
from flask_jwt_extended import jwt_required
from .res import success_response
from jsonschema import ValidationError


@bp.route('/upload', methods=['POST'])
@jwt_required
def upload_image():
    if request.files and 'image' in request.files:
        filename = photos.save(request.files['image'])
        return success_response({'filename': filename, 'image_url': photos.url(filename)})
    else:
        raise ValidationError('Invalid parameter')


@bp.route('/upload/<path:filename>', methods=['GET'])
def download_file(filename):
    file = os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], filename)
    directory = os.path.dirname(file)
    fn = os.path.basename(file)
    return send_from_directory(directory, fn)
