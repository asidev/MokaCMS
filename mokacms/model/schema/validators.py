#!/usr/bin/env/python

from colander import Invalid
import urllib.parse
import re

__all__ = ["URI", "Path"]
identifier_regex = re.compile(r'^[^\d\W]\w*$')


def URI(node, value):
    res = urllib.parse.urlparse(value)
    if not res.path.startswith("/"):
        raise Invalid(node, '{} has wrong path {}'.format(value,
                                                          res.path))


def Path(node, value):
    URI(node, value)
    if not value.startswith("/"):
        raise Invalid(node, "not a path: %r".format(value))


def PythonIdentifier(node, value):
    if identifier_regex.match(value) is None:
        raise Invalid(node, "%r is not a valid Python identifier".format(value))
