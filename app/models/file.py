# -*- coding:utf-8 -*-
"""保存文件所属信息"""

from app.extensions import db
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER,TIMESTAMP

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship


class FileInfo(db.Model):
    """文件所属信息"""

    __tablename__ = 'file_info'
    __table_args__ = {'mysql_collate': 'utf8mb4_general_ci'}

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    filename = Column(VARCHAR(200), nullable=False, comment='文件名')
    creator_id = Column(INTEGER,
                        ForeignKey('user.id', name='fk_file_info_creator_id', ondelete='NULL', onupdate='CASCADE'),
                        nullable=False, comment='文件创建者id')

    owner_id = Column(INTEGER,
                      ForeignKey('user.id', name='fk_file_info_owner_id', ondelete='NULL', onupdate='CASCADE'),
                      nullable=False, comment='所有者id')

    created_at = Column(TIMESTAMP, nullable=False, comment='创建时间')

    # owner = relationship('User')
    # creator = relationship('User')

    def __repr__(self):
        return 'FileInfo<{}, {}>'.format(self.id, self.filename)

