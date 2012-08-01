#!/usr/bin/env python
import logging
import os
import sys
import traceback
from cement.core import (handler,
                         hook,
                         foundation)

from mokacms.cli.database import MokaDatabaseController
from mokacms.cli.module import MokaModuleController
from mokacms.cli.compile import MokaCompileController
from mokacms.cli.base import MokaBaseController
from mokacms.cli.output import MokaOutputHandler
import cement.ext.ext_json
from pyramid.decorator import reify
from pyramid.paster import bootstrap
from pymongo import Connection


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
    def request(self):
        req = self.pyramid_app['request']
        req.mdb = self.mdb
        return req

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

        try:
            env = bootstrap(self.pargs.ini)

        except:
            self.log.error("Cannot bootstrap application")
            raise

        def cleanup(_):
            self.log.debug("Calling pyramid app closer")
            env['closer']()

        hook.register("pre_close", cleanup)
        return env

    @reify
    def pyramid_settings(self):
        return self.pyramid_app['registry'].settings

    def render(self, data=None):
        ctrl_data = None
        try:
            ctrl_data = self.controller.result

        except AttributeError:
            pass
        
        if data and ctrl_data:
            data.update(ctrl_data)
        elif not data and ctrl_data:
            data = ctrl_data

        return super(MokaApp, self).render(data)


def main():
    app = MokaApp()
    handler.register(MokaDatabaseController)
    handler.register(MokaModuleController)
    handler.register(MokaCompileController)
    cement.ext.ext_json.load()
    data = dict(success=False)

    try:
        app.setup()
        app.args.add_argument("-i", "--ini", action="store",
            help="Path to the pyramid config. Defaults to {}".format(DEFAULT_INI),
            default=DEFAULT_INI)

        app.run()

    except Exception as e:
        typ, value, tb = sys.exc_info()
        ftb = traceback.format_tb(tb)
        app.log.fatal("{}: {}".format(typ.__name__, value))
        app.log.fatal("".join(ftb))
        data = dict(success=False,
                    message=str(value),
                    exception=typ.__name__,
                    traceback=ftb)
    else:
        data = dict(success=True)

    finally:
        rendered = app.render(data)
        if rendered:
            print(rendered)

        app.close()


if __name__ == '__main__':
    main()
