#!/usr/bin/env python
from .base import MokaModel
from .schema import ModuleSchema


class Module(MokaModel):
    collection_name = 'modules'
    default_get_attr = 'name'
    Schema = ModuleSchema