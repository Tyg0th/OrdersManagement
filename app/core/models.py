import datetime

from sqlalchemy.ext.declarative import declared_attr
from app import db


class TimestampedModel(object):
    @declared_attr
    def created_at(cls):
        # A timestamp representing when this object was created.
        return db.Column(db.DateTime, default=datetime.datetime.now())
    @declared_attr
    def updated_at(cls):
        # A timestamp reprensenting when this object was last updated.
        return db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())


class IsDeleted(object):
    @declared_attr
    def db_status(cls):
        # A timestamp representing when this object was created.
        return db.Column(db.Boolean, default=True)