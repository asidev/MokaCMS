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
    def find(cls, db, *args, **kwargs):
        raw = kwargs.pop("raw_", False)
        def conv(obj):
            return obj if raw else cls(obj)

        return (conv(p) for p in cls.collection(db).find(*args, **kwargs) if p)

    @classmethod
    def find_one(cls, db, *args, **kwargs):
        raw = kwargs.pop("raw_", False)
        def conv(obj):
            return obj if raw else cls(obj)

        res = cls.collection(db).find_one(*args, **kwargs)
        if not res:
            raise NoResult(args)
        return conv(res)

    @classmethod
    def all(cls, db, raw=False):
        return cls.find(db, raw_=raw)

    @classmethod
    def get(cls, db, value, raw=False):
        return cls.find_one(db, {cls.default_get_attr: value})

    @classmethod
    def get_by(cls, db, attr, value, raw=False):
        return cls.find_one(db, {attr: value}, raw_=raw)

    def __init__(self, objinfo__=None, **kwargs):
        info = objinfo__ if objinfo__ else kwargs
        object.__setattr__(self, "_objinfo", {})
        self._objinfo = self.schema.deserialize(info)
        self._updated_values = set()
        self._objid = info.get('_id', None)

    def __getattr__(self, attr):
        try:
            return self._objinfo[attr]

        except:
            raise AttributeError(attr)

    def __setattr__(self, attr, value):
        if attr in self._objinfo:
            self._updated_attrs.add(attr)
            self._objinfo[attr] = value
        else:
            object.__setattr__(self, attr, value)

    def asdict(self):
        return self._objinfo.copy()

    def flatten(self):
        return self.schema.flatten(self._objinfo)

    def unflatten(self, data):
        self._objinfo = self.schema.unflatten(data)

    def save(self, db):
        if self._objid:
            self.__class__.log.debug("Updating object %s", self._objid)
            values = {k: self._objinfo[k] for k in self._updated_attrs}
            self.collection(db).update({"_id": self._objid}, {"$set": values})
            self._updated_attrs = set()
        else:
            self.__class__.log.debug("Creating object %s", self._objinfo)
            self._objid = self.collection(db).insert(self._objinfo)

    def delete(self, db):
        if self._objid:
            self.log.info("Dropping object %s", self._objid)
            self.collection(db).drop({"_id": self._objid})
            del self._objinfo
            del self._id
        else:
            self.log.warn("Cannot drop non-created object: %s", self._objinfo)