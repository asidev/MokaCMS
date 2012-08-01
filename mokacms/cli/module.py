#!/usr/bin/env python
from . base import MokaBaseController
from mokacms.model import Module
from cement.core import controller
from pyramid.path import DottedNameResolver


class MokaModuleController(MokaBaseController):
    class Meta:
        label = 'module'
        description = 'Manage modules'
        arguments = [
            (['module'],dict(help="module_name", nargs=1))
        ]

    @controller.expose(aliases=["import"])
    def import_module(self):
        module_name = self.pargs.module[0]
        self.log.info("Importing module %s" % module_name)
        resolver = DottedNameResolver()
        try:
            module = resolver.resolve(module_name)

        except Exception as e:
            self.log.error("Cannot import module: %s" % e)

        else:
            mod = Module.inspect(module)
            mod.save(self.app.mdb)
            self.log.info("Saved module %s to database" % (mod))
