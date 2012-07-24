#!/usr/bin/env/python

from colander import (Invalid,
                      SchemaType,
                      null)
import urllib.parse
__all__ = ['URI', 'UrlPath']


class URI(SchemaType):
    def serialize(self, node, appstruct):
        if appstruct is null or appstruct is None:
            return null

        if not isinstance(appstruct, str):
            raise Invalid(node, '%r is not a string'.format(appstruct))

        res = urllib.parse.urlparse(appstruct)
        if not res.path.startswith("/"):
            raise Invalid(node, '{} has wrong path {}'.format(appstruct,
                                                              res.path))

        return appstruct

    def deserialize(self, node, cstruct):
        if cstruct is null or cstruct is None:
            return null

        if not isinstance(cstruct, str):
            raise Invalid(node, '%r is not a string'.format(cstruct))

        res = urllib.parse.urlparse(cstruct)
        if not res.path.startswith("/"):
            raise Invalid(node, '{} has wrong path {}'.format(cstruct,
                                                              res.path))

        return cstruct


class UrlPath(SchemaType):
    def serialize(self, node, appstruct):
        if appstruct is null or appstruct is None:
            return null

        uri_validator = URI()
        try:
            uri_validator.serialize(None, appstruct)

        except Invalid as e:
            raise Invalid(node, e.msg)

        if not appstruct.startswith("/"):
            raise Invalid("not a path: %r".format(appstruct))

        return appstruct

    def deserialize(self, node, cstruct):
        if cstruct is null or cstruct is None:
            return null

        uri_validator = URI()
        try:
            uri_validator.deserialize(None, cstruct)

        except Invalid as e:
            raise Invalid(node, e.msg)

        if not cstruct.startswith("/"):
            raise Invalid("not a path: %r".format(cstruct))

        return cstruct
