#!/usr/bin/env python
import colander
from mokacms.utils import clean_html
from .validators import Path
__all__ = ['PageSchema']
CHANGEFREQ = ('always', 'hourly', 'daily', 'weekly',
              'monthly', 'yearly', 'never')


class SitemapSchema(colander.MappingSchema):
    priority = colander.SchemaNode(colander.Float(),
                                   validator=colander.Range(min=0.0, max=1.0),
                                   default=0.5, missing=0.5)
    lastmod = colander.SchemaNode(colander.DateTime(), default=None,
                                  missing=None)
    changefreq = colander.SchemaNode(colander.String(),
                                     validator=colander.OneOf(CHANGEFREQ),
                                     default=None, missing=None)

class TranslationSchema(colander.MappingSchema):
    language = colander.SchemaNode(colander.String())
    url = colander.SchemaNode(colander.String(), validator=Path)


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
    url = colander.SchemaNode(colander.String(), validator=Path)
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
    sitemap = SitemapSchema(missing={}, default={})
