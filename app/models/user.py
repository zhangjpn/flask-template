# -*- coding:utf-8 -*-
from datetime import datetime, timedelta, timezone

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.dialects.mysql import TINYINT, TIMESTAMP, VARCHAR, INTEGER
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from . import OutputMixin

tz = timezone(timedelta(hours=8))


class User(db.Model, OutputMixin):
    """
    用户
    """

    __tablename__ = 'user'
    __table_args__ = {'mysql_collate': 'utf8mb4_general_ci'}

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)  # 用户id/管理员id都是同一个

    nick_name = Column(VARCHAR(100))

    mobile = Column(VARCHAR(20))  # 没用

    union_id = Column(VARCHAR(174), unique=True, nullable=True)
    app_id = Column(VARCHAR(200))
    open_id = Column(VARCHAR(174), nullable=True)
    avatar_url = Column(VARCHAR(1024), nullable=True)
    country = Column(VARCHAR(30), nullable=True)
    city = Column(VARCHAR(30), nullable=True)
    gender = Column(TINYINT, nullable=True)
    language = Column(VARCHAR(30), nullable=True)
    province = Column(VARCHAR(30), nullable=True)
    session_key = Column(VARCHAR(200), nullable=True)
    # 微信用户的电话号码信息
    phone_number = Column(VARCHAR(100), nullable=True, comment='微信小程序用户手机号，包含区号信息')
    pure_phone_number = Column(VARCHAR(100), nullable=True, comment='微信小程序用户手机号， 不包含区号信息')
    country_code = Column(VARCHAR(10), nullable=True, comment='区号代码')

    # 管理员相关字段
    admin_login_name = Column(VARCHAR(30), unique=True)
    admin_pwd_hash = Column(VARCHAR(1024), nullable=True)
    admin_role_id = Column(INTEGER(unsigned=True), ForeignKey('role.id'))
    admin_last_login_at = Column(TIMESTAMP(timezone=True), nullable=True)

    role = relationship('Role', back_populates='users')

    def __repr__(self):
        return "User:<%s %s>" % (self.id, self.username)

    def set_password(self, password):
        self.admin_pwd_hash = generate_password_hash(password.encode(encoding='utf-8'))

    def check_password(self, password):
        return check_password_hash(self.admin_pwd_hash, password)

    def set_login_time(self):
        self.admin_last_login_at = datetime.now()

    def admin_to_json(self):
        login_time = None
        if self.admin_last_login_at:
            # 读取时的日期为当前所在时区的日期对象，虽然没有时区信息，但已经是本地时间，所以只需使用astimezone()将时区信息补上即可
            login_time = self.admin_last_login_at.astimezone().isoformat()
        return {
            'admin_login_name': self.admin_login_name,
            'admin_role_id': self.admin_role_id,
            'admin_last_login_at': login_time,
            'role': self.role.to_json(),
        }

    @classmethod
    def create_from_wx(cls, **kwargs):
        """通过微信信息创建用户"""
        user = cls()
        for k, v in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, v)
        return user

    def to_json(self, rel=None):
        return {
            'nickName': self.nick_name,
            'avatarUrl': self.avatar_url,
            'province': self.province,
            'country': self.country,
            'city': self.city,
            'gender': self.gender,
            'id': self.id,
        }

    def save_user_info(self, **kwargs):
        fields = ['nick_name', 'avatar_url', 'gender', 'province', 'city', 'country', 'mobile']
        for k, v in kwargs.items():
            if k in fields:
                setattr(self, k, v)


role_has_permissions = Table('role_permissions', db.Model.metadata,
                             Column(INTEGER(unsigned=True), ForeignKey('role.id'), name='role_id', primary_key=True),
                             Column(INTEGER(unsigned=True), ForeignKey('permission.id'), name='permission_id',
                                    primary_key=True),
                             )


class Role(db.Model, OutputMixin):
    """角色"""

    __tablename__ = 'role'
    __table_args__ = {'mysql_collate': 'utf8mb4_general_ci'}

    id = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(VARCHAR(30), unique=True)
    permissions = relationship('Permission', secondary=role_has_permissions, back_populates='roles')

    users = relationship('User', back_populates='role')

    def __repr__(self):
        return "Role<%s %s>" % (self.id, self.name)

    def to_json(self, rel=None):
        return {
            'id': self.id,
            'name': self.name,
            'permissions': [i.to_json() for i in self.permissions]
        }


class Permission(db.Model, OutputMixin):
    """权限"""

    __tablename__ = 'permission'
    __table_args__ = {'mysql_collate': 'utf8mb4_general_ci'}

    id = Column(INTEGER(unsigned=True), primary_key=True)
    name = Column(VARCHAR(30), unique=True)
    roles = relationship('Role', secondary=role_has_permissions, back_populates='permissions')

    def __repr__(self):
        return "Permission<%s %s>" % (self.id, self.name)

    def to_json(self, rel=None):
        return {
            'id': self.id,
            'name': self.name,
        }
