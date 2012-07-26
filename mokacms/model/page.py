#!/usr/bin/env python
from .base import MokaModel
from .theme import Theme
from .schema import (PageSchema,
                     RedirectSchema)
from pyramid.path import DottedNameResolver


class Page(MokaModel):
    collection_name = 'pages'
    default_get_attr = 'url'

    def __new__(cls, objinfo__=None, **kwargs):
        info = objinfo__ if objinfo__ else kwargs
        if "redirect" in info:
            return super(Page, cls).__new__(Redirect, objinfo__, **kwargs)

        return super(Page, cls).__new__(Content, objinfo__, **kwargs)

    @classmethod
    def homepage(cls, db, lang):
        cls.log.debug("Getting homepage for lang {}".format(lang))
        page = db.pages.find_one(dict(homepage=True, language=lang))
        if not page:
            cls.log.error("Cannot find any homepage for lang {}".format(lang))
        return cls(page)


class Content(Page):
    Schema = PageSchema

    def run_widgets(self, request):
        theme = request.registry.settings['mokacms.theme']
        db = request.mdb
        self.log.debug("Running widgets for %s, (theme: %s)", self, theme)
        resolver = DottedNameResolver()
        theme = Theme.get(db, theme)
        widgets = []
        result = {}

        for template in theme.templates:
            if template['file'] == self.template:
                widgets = template["widgets"]

        self.log.debug("Found widgets: %s", widgets)
        for widget in widgets:
            cname = widget['name']
            args = {a['name']: a['value'] for a in widget['args']}
            self.log.debug("Excecuting %s with args %s", cname, args)
            try:
                result[cname] = dict(
                    args=widget['args'],
                    result=resolver.resolve(cname)(request, **args)
                )

            except:
                self.log.exception("Error while running widget %s with args %s",
                                   cname, args)
                raise

        return result

class Redirect(Page):
    Schema = RedirectSchema
