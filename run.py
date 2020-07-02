# -*-coding:utf-8 -*-


from app import create_app
from app.extensions import db
from flask_migrate import Migrate
from config import DevConfig

app = create_app(DevConfig)

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict()


if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)
