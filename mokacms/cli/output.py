#!/usr/bin/env python
from cement.core import output
import pprint


class MokaOutputHandler(output.CementOutputHandler):
    class Meta:
        label = 'moka'

    def render(self, data, template=None):
        if not template:
            data.pop('success', None)
            if data:
                print("Result data:")
                pprint.pprint(data)

        else:
            raise NotImplementedError()
