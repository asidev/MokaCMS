#!/usr/bin/env python
import sys
from cement.core import (controller, backend)


class MokaBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "CLI Access to MokaCMS features"

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        self.log.error(self.app.args.format_help())
