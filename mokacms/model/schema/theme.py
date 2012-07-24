#!/usr/bin/env python
import colander
from .types import UrlPath
__all__ = ['ThemeSchema']


class TemplateWidgetArgSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    value = colander.SchemaNode(colander.String())


class TemplateWidgetArgsSchema(colander.SequenceSchema):
    arg = TemplateWidgetArgSchema()


class TemplateWidgetSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    args = TemplateWidgetArgsSchema()


class TemplateWidgetsSchema(colander.SequenceSchema):
    widget = TemplateWidgetSchema()


class TemplateNameSchema(colander.MappingSchema):
    language = colander.SchemaNode(colander.String())
    text = colander.SchemaNode(colander.String())


class TemplateNamesSchema(colander.SequenceSchema):
    name = TemplateNameSchema()


class TemplateSchema(colander.MappingSchema):
    name = TemplateNamesSchema()
    file = colander.SchemaNode(UrlPath())
    widgets = TemplateWidgetsSchema()


class TemplatesSchema(colander.SequenceSchema):
    template = TemplateSchema()


class ThemeSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    templates = TemplatesSchema()
