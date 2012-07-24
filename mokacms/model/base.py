#!/usr/bin/env python
import logging
from mokacms.utils import classproperty
from mokacms.model.exceptions import NoResult

class MokaModel:

    @classproperty
    @classmethod
    def log(cls):
        return logging.getLogger(cls.__module__)

    @classmethod
    def collection(cls, db):
        return getattr(db, cls.collection_name)

    @classmethod
    def find(cls, db, raw=False, *args, **kwargs):
        def conv(obj):
            return obj if raw else cls(obj)

        return (conv(p) for p in cls.collection(db).find(*args, **kwargs) if p)

    @classmethod
    def find_one(cls, db, raw=False, *args, **kwargs):
        def conv(obj):
            return obj if raw else cls(obj)

        res = cls.collection(db).find_one(*args, **kwargs)
        if not res:
            raise NoResult(args)
        return conv(res)

    @classmethod
    def all(cls, db, raw=False):
        return cls.find(db, raw)

    @classmethod
    def get(cls, db, value, raw=False):
        return cls.find_one(db, raw, {cls.default_get_attr: value})

    @classmethod
    def get_by(cls, db, attr, value, raw=False):
        return cls.find_one(db, raw, {attr: value})

    def __init__(self, objinfo__=None, **kwargs):
        info = objinfo__ if objinfo__ else kwargs
        self.__objinfo = self.schema.deserialize(info)
        if "_id" in info:
            self._id = info['_id']

    def __getattr__(self, attr):
        try:
            return self.__objinfo[attr]

        except:
            raise AttributeError(attr)

    def to_dict(self):
        return self.__objinfo.copy()

    def flatten(self):
        return self.schema.flatten(self.__objinfo)

    def unflatten(self, data):
        self.__objinfo = self.schema.unflatten(data)