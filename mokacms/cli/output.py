#!/usr/bin/env python
from cement.core import output


class MokaOutputHandler(output.CementOutputHandler):
    class Meta:
        label = 'moka'

    def render(self, data, template=None):
        for k, v in data.items():
            print("{} => {}".format(k, v))
