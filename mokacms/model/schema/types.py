#!/usr/bin/env/python

from colander import (SchemaType,
                      null)
__all__ = ['Raw']


class Raw(SchemaType):
    def serialize(self, node, appstruct):
        if appstruct is null or appstruct is None:
            return null

        return appstruct

    def deserialize(self, node, cstruct):
        if cstruct is null or cstruct is None:
            return null

        return cstruct
