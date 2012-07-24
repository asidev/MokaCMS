#!/usr/bin/env python
import colander
from mokacms.model.schema.types import (URI,
                           UrlPath)
__all__ = ['RedirectSchema']


class RedirectToSchema(colander.MappingSchema):
    url = colander.SchemaNode(URI())
    code = colander.SchemaNode(colander.Int(),
                               validator=colander.Range(300, 307))


class RedirectSchema(colander.MappingSchema):
    url = colander.SchemaNode(UrlPath())
    redirect = RedirectToSchema()
    enabled = colander.SchemaNode(colander.Boolean(),
                                  default=False, missing=False)

