#!/usr/bin/env/python

from colander import Invalid
from pyramid.path import DottedNameResolver
import urllib.parse

__all__ = ['DottedPythonName', "URI", "Path"]


def DottedPythonName(node, value):

    resolver = DottedNameResolver()
    try:
        resolver.resolve(value)

    except ImportError as e:
        raise Invalid(node, str(e))


def URI(node, value):
    res = urllib.parse.urlparse(value)
    if not res.path.startswith("/"):
        raise Invalid(node, '{} has wrong path {}'.format(value,
                                                          res.path))


def Path(node, value):
    URI(node, value)
    if not value.startswith("/"):
        raise Invalid(node, "not a path: %r".format(value))
