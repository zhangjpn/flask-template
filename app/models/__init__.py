# -*-coding:utf-8 -*-

import json
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy.ext.declarative import DeclarativeMeta


class OutputMixin(object):
    RELATIONSHIPS_TO_DICT = False

    def __iter__(self):
        return self.to_dict().items()

    @staticmethod
    def format(column):

        if isinstance(column, (str, int, float, bool)):
            return column
        if isinstance(column, Decimal):
            return float(column)
        if isinstance(column, datetime):
            return column.astimezone().isoformat()
        if isinstance(column, date):
            return column.strftime('%Y-%m-%d')
        return column

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: self.format(getattr(self, attr))
               for attr, column in self.__mapper__.c.items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref and backref == relation.backref:  # TODO:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                elif isinstance(value.__class__, Decimal):
                    res[relation.key] = float(value)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def to_json(self, rel=None):
        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()

        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)
