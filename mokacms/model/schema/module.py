#!/usr/bin/env python
import colander
from .types import (DottedPythonName,
                    Raw)
from .validators import PythonIdentifier


class ModuleLabel(colander.MappingSchema):
    language = colander.SchemaNode(colander.String())
    name = colander.SchemaNode(colander.String())


class ModuleLabels(colander.SequenceSchema):
    label = ModuleLabel()


class ModuleFunctionArg(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), validator=PythonIdentifier)
    default = colander.SchemaNode(Raw(), missing=None, default=None)


class ModuleFunctionArgs(colander.SequenceSchema):
    arg = ModuleFunctionArg()


class ModuleFunction(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), validator=PythonIdentifier)
    args = ModuleFunctionArgs()


class ModuleFunctions(colander.SequenceSchema):
    function = ModuleFunction()


class ModuleSchema(colander.MappingSchema):
    module = colander.SchemaNode(DottedPythonName())
    labels = ModuleLabels()
    functions = ModuleFunctions()
    # assets ?
