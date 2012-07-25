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
from pyramid.paster import bootstrap
from pymongo import Connection
import logging


DEFAULT_INI_NAME =  'moka.ini'
if "MOKA_INI" in os.environ:
    DEFAULT_INI_NAME = os.environ['MOKA_INI']
MOKA_ROOT = os.path.realpath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         '..', '..'))
DEFAULT_INI = os.path.join(MOKA_ROOT, DEFAULT_INI_NAME)


class MokaApp(foundation.CementApp):
    root_path = MOKA_ROOT

    class Meta:
        label = 'moka'
        base_controller = MokaBaseController
        output_handler = MokaOutputHandler

    @reify
    def mdb(self):
        r = self.pyramid_app['registry']
        return r.mongodb_connection[r.mongodb_database]

    @reify
    def pyramid_app(self):
        self.log.debug("Bootstrapping pyramid application")
        # setup logging
        logger = logging.getLogger("mokacms")
        current_level = self.log.level()
        logger.setLevel(current_level)
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s: [mokacms] %(message)s")
        ch.setLevel(current_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        env = bootstrap(self.pargs.ini)

        def cleanup(_):
            self.log.debug("Calling pyramid app closer")
            env['closer']()

        hook.register("pre_close", cleanup)
        return env

    @reify
    def pyramid_settings(self):
        return self.pyramid_app['registry'].settings

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
