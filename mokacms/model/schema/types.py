#!/usr/bin/env/python

import colander
from pyramid.path import DottedNameResolver
__all__ = ['Raw', 'Integer', 'Float', 'Boolean', 'DottedPythonName']
colander.null = None


class Integer(colander.Int):
    def serialize(self, node, appstruct):
        return int(super(Integer, self).serialize(node, appstruct))


class Float(colander.Float):
    def serialize(self, node, appstruct):
        return float(super(Float, self).serialize(node, appstruct))


class Boolean(colander.Boolean):
    def serialize(self, node, appstruct):
        return appstruct


class Raw(colander.SchemaType):
    def serialize(self, node, appstruct):
        if appstruct is colander.null or appstruct is None:
            return colander.null

        return appstruct

    def deserialize(self, node, cstruct):
        if cstruct is colander.null or cstruct is None:
            return colander.null

        return cstruct


class DottedPythonName(colander.SchemaType):

    def serialize(self, node, appstruct):
        if appstruct is colander.null or appstruct is None:
            return colander.null

        if not hasattr(appstruct, "__module__"):
            return appstruct.__name__

        return "{0}.{1}".format(appstruct.__module__, appstruct.__name__)

    def deserialize(self, node, cstruct):
        if cstruct is colander.null or cstruct is None:
            return colander.null

        resolver = DottedNameResolver()
        try:
            return resolver.resolve(cstruct)

        except ImportError as e:
            raise Invalid(node, str(e))
