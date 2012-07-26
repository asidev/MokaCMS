#!/usr/bin/env python
import colander
from .types import (Raw,
                    DottedPythonName)
from .validators import PythonIdentifier


class WidgetArgSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), validator=PythonIdentifier)
    value = colander.SchemaNode(Raw())


class WidgetArgsSchema(colander.SequenceSchema):
    arg = WidgetArgSchema()


class WidgetSchema(colander.MappingSchema):
    callable = colander.SchemaNode(DottedPythonName())
    args = WidgetArgsSchema()
