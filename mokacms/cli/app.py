#!/usr/bin/env python
import os
from cement.core import (handler,
                         hook,
                         foundation)

from mokacms.cli.database import MokaDatabaseController
from mokacms.cli.base import MokaBaseController
from mokacms.cli.output import MokaOutputHandler
import cement.ext.ext_json
from pyramid.decorator import reify
from pymongo import Connection


DEFAULT_INI = os.path.realpath(
                os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '..', '..', 'moka.ini'))
if "MOKA_INI" in os.environ:
    DEFAULT_INI = os.environ['MOKA_INI']


class MokaApp(foundation.CementApp):
    class Meta:
        label = 'moka'
        base_controller = MokaBaseController
        output_handler = MokaOutputHandler

    @reify
    def pyramid_config(self):
        self.log.debug("Parsing pyramid config")
        sect = "app:main"
        self.config.parse_file(self.pargs.ini)
        return {k: self.config.get(sect, k) for k in self.config.keys(sect)}


    @reify
    def mongodb_connection(self):
        pfx = "mongo"
        self.log.debug("Connecting to mongodb")
        conn = Connection(**{
            k.replace("mongodb.", ""): v for k,v in self.pyramid_config.items()
            if k.startswith("mongodb.") and k != "mongodb.database"
        })

        def cleanup(_):
            self.log.debug("Closing connection to mongodb")
            conn.close()

        hook.register("pre_close", cleanup)
        return conn

    @reify
    def mdb(self):
        return self.mongodb_connection[self.pyramid_config['mongodb.database']]

    def render(self):
        try:
            data = self.controller.result

        except AttributeError:
            pass

        else:
            return super(MokaApp, self).render(data)


def main():
    app = MokaApp()
    handler.register(MokaDatabaseController)
    cement.ext.ext_json.load()

    try:
        app.setup()
        app.args.add_argument("-i", "--ini", action="store",
            help="Path to the pyramid config. Defaults to {}".format(DEFAULT_INI),
            default=DEFAULT_INI)

        app.run()
        data = app.render()
        if data:
            print(data)

    finally:
        app.close()


if __name__ == '__main__':
    main()
