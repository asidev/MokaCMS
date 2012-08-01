#!/usr/bin/env python
import os
import shutil
from . base import MokaBaseController
from cement.core import controller
from mokacms.model import (Page,
                           Menu)
from pyramid.renderers import render_to_response


class MokaCompileController(MokaBaseController):
    class Meta:
        label = 'compile'
        description = 'Compile website to html'
        arguments = [
            (['outdir'],
             dict(help="output directory for generated HTML",
             nargs=1))
        ]

    @controller.expose()
    def default(self):
        outdir = os.path.realpath(self.pargs.outdir[0])
        self.log.info("Compiling pages to {}".format(outdir))
        pages = Page.all(self.app.mdb)
        menus = {}
        for page in pages:
            self.log.info("[PAGE] {}".format(page.url))
            if hasattr(page, "redirect"):
                self.log.warn("Skipping page {} (redirect)".format(page.url))
                continue

            try:
                menu = menus[page.language]

            except KeyError:
                menus[page.language] = [m.serialize() for m in
                                        Menu.get(self.app.mdb, page.language)]
                menu = menus[page.language]

            page_d = page.serialize()
            page_d['widgets'] = page.run_widgets(self.app.request)

            dest_file = os.path.join(outdir, page.url[1:])
            dest_dir = os.path.dirname(dest_file)
            try:
                os.makedirs(dest_dir)
                self.log.info("[MKDIR] {}".format(dest_dir))

            except OSError as e:
                if e.errno != 17:
                    raise

            with open(dest_file, "wb") as f:
                response = render_to_response(page.template,
                                              dict(page=page_d, menus=menu),
                                              request=self.app.request)
                #shutil.copyfileobj(response.body_file, f)
                f.write(response.body)
