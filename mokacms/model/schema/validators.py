#!/usr/bin/env/python

from colander import Invalid
import urllib.parse

__all__ = ["URI", "Path"]


def URI(node, value):
    res = urllib.parse.urlparse(value)
    if not res.path.startswith("/"):
        raise Invalid(node, '{} has wrong path {}'.format(value,
                                                          res.path))


def Path(node, value):
    URI(node, value)
    if not value.startswith("/"):
        raise Invalid(node, "not a path: %r".format(value))
