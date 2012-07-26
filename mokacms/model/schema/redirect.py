#!/usr/bin/env python
import colander
from .validators import (Path,
                         URI)
__all__ = ['RedirectSchema']


class RedirectToSchema(colander.MappingSchema):
    url = colander.SchemaNode(colander.String(), validator=URI)
    code = colander.SchemaNode(colander.Int(),
                               validator=colander.Range(300, 307))


class RedirectSchema(colander.MappingSchema):
    url = colander.SchemaNode(colander.String(), validator=Path)
    redirect = RedirectToSchema()
    enabled = colander.SchemaNode(colander.Boolean(),
                                  default=False, missing=False)

