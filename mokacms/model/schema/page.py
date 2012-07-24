#!/usr/bin/env python
import colander
from mokacms.utils import clean_html
from mokacms.model.schema.types import UrlPath
__all__ = ['PageSchema']


class TranslationSchema(colander.MappingSchema):
    language = colander.SchemaNode(colander.String())
    url = colander.SchemaNode(UrlPath())


class TranslationsSchema(colander.SequenceSchema):
    translation = TranslationSchema()


class ContentSchema(colander.MappingSchema):
    body = colander.SchemaNode(colander.String(),
                               preparer=clean_html)


class ContentsSchema(colander.SequenceSchema):
    content = ContentSchema()


class MetaHeaderAttrSchema(colander.MappingSchema):
    key = colander.SchemaNode(colander.String())
    value = colander.SchemaNode(colander.String())


class MetaHeaderAttrsSchema(colander.SequenceSchema):
    attr = MetaHeaderAttrSchema()


class MetaHeaderSchema(colander.MappingSchema):
    attrs = MetaHeaderAttrsSchema()
    value = colander.SchemaNode(colander.String(), default="", missing="")


class MetaHeadersSchema(colander.SequenceSchema):
    meta = MetaHeaderSchema()


class PageHeadSchema(colander.MappingSchema):
    meta = MetaHeadersSchema()


class PageSchema(colander.MappingSchema):
    url = colander.SchemaNode(UrlPath())
    template = colander.SchemaNode(colander.String(),
                                   default=None)
    language = colander.SchemaNode(colander.String(),
                                   default=None)
    title = colander.SchemaNode(colander.String(),
                                default=None)
    homepage = colander.SchemaNode(colander.Boolean(),
                                   default=False)
    enabled = colander.SchemaNode(colander.Boolean(),
                                  default=False)
    head = PageHeadSchema()
    contents = ContentsSchema()
    translations = TranslationsSchema()
