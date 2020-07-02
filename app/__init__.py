# -*-coding:utf-8 -*-

from flask import Flask

from flask_uploads import configure_uploads
from flask.json import JSONEncoder
from sqlalchemy.ext.declarative import DeclarativeMeta


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return obj.to_dict()
        return super(CustomJSONEncoder, self).default(obj)


def create_app(config):
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.config.from_object(config)

    from .extensions import jwt, db, cors, photos, documents, wx, migrate
    wx.init_app(app)
    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    configure_uploads(app, photos)
    configure_uploads(app, documents)
    migrate.init_app(app, db)
    from app.errors import bp as errors_bp
    from app.api import bp as api_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
