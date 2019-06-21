# -*- coding:utf-8 -*-

from flask_migrate import Migrate, MigrateCommand
from app.extensions import db
from flask_script import Manager
from app.extensions import app

manager = Manager(app)

# 创建数据库迁移对象
migrate = Migrate(app, db)

# 添加操作命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
