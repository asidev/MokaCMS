#!/usr/bin/env python
from .base import MokaModel
from .schema import ThemeSchema


class Theme(MokaModel):
    collection_name = 'themes'
    default_get_attr = 'name'
    Schema = ThemeSchema
