#!/usr/bin/env python
from .base import MokaModel
from .schema import MenuSchema


class Menu(MokaModel):
    collection_name = 'menus'
    default_get_attr = 'translations.language'
    schema = MenuSchema()

    @classmethod
    def get(cls, db, value, raw=False):
        return cls.find(db, raw, {cls.default_get_attr: value})
