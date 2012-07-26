#!/usr/bin/env python
import inspect
from .base import MokaModel
from .schema import ModuleSchema


class Module(MokaModel):
    collection_name = 'modules'
    default_get_attr = 'module'
    Schema = ModuleSchema

    @classmethod
    def inspect(cls, module):
        """ Inspect a module and return a new Module model"""

        functions = []
        module_name = module.__name__
        module_version = getattr(module, "__version__", None)
        labels = getattr(module, "__labels__", [])

        for callable_name in module.__all__:
            function_spec = []
            cls.log.debug("Inspecting %s.%s", module_name, callable_name)
            try:
                obj = getattr(module, callable_name)

            except AttributeError:
                cls.log.error("Cannot import name %s from %s, skipping",
                               callable_name, module_name)
                continue

            if not inspect.isclass(obj) and not inspect.isfunction(obj):
                cls.log.error("%s.%s is neither a class or a function, skipping",
                               module_name, callable_name)
                continue

            fun = obj.__call__ if inspect.isclass(obj) else obj

            spec = inspect.getfullargspec(fun)
            def_idx = len(spec.args) - len(spec.defaults)
            for i, arg in enumerate(spec.args):
                if i == 0:
                    # first arg is either request or self, so skip it
                    continue

                default = None if i < def_idx else spec.defaults[i - def_idx]
                function_spec.append(dict(name=arg, value=default))

            full_name = "%s.%s" % (module_name, callable_name)
            cls.log.info("Adding %s with args %s",
                          full_name, function_spec)
            functions.append(dict(name=callable_name, args=function_spec))

        opts = dict(module=module_name, version=module_version, labels=labels,
                   functions=functions)
        cls.log.info("Creating module: %s", opts)
        return cls(**opts)
