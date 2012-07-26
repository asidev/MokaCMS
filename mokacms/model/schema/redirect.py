#!/usr/bin/env python
import colander
from .validators import (Path,
                         URI)
from .types import (Integer,
                    Boolean)
__all__ = ['RedirectSchema']


class RedirectToSchema(colander.MappingSchema):
    url = colander.SchemaNode(colander.String(), validator=URI)
    code = colander.SchemaNode(Integer(),
                               validator=colander.Range(300, 307))


class RedirectSchema(colander.MappingSchema):
    url = colander.SchemaNode(colander.String(), validator=Path)
    redirect = RedirectToSchema()
    enabled = colander.SchemaNode(Boolean(),
                                  default=False, missing=False)

