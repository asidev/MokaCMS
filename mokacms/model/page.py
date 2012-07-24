#!/usr/bin/env python
from .base import MokaModel
from .schema import (PageSchema,
                     RedirectSchema)

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
    schema = PageSchema()


class Redirect(Page):
    schema = RedirectSchema()

