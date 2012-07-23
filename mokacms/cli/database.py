#!/usr/bin/env python

from cement.core import controller
from . base import MokaBaseController

class MokaDatabaseController(MokaBaseController):
    class Meta:
        label = 'database'
        description = 'Manage database-related stuff'
        config_defaults = dict()
