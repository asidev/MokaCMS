#!/usr/bin/env python
import os
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
             nargs=1)),
            (['--redirect-as', '-r'],
            dict(help="Write redirects.",
                 choices=('html', 'php', 'asp', 'js', 'skip'),
                 default="html")),
            (['--index', '-I'],
             dict(help="Directory index file name, without ext.",
                  default="index"))
        ]

    def write_redirect(self, from_, to, dest):
        self.log.info("[REDIR] [{}] {} -> {}"\
            .format(self.pargs.redirect_as.upper(),
                    from_, to))
        dest = dest.replace(".html", "")

        if self.pargs.redirect_as in ('html', 'js'):
            content = self.html_redirect(to, self.pargs.redirect_as)
            dest = dest + ".html"

        elif self.pargs.redirect_as == 'php':
            content = self.php_redirect(to)
            dest = dest + ".php"

        elif self.pargs.redirect_as == 'asp':
            content = self.asp_redirect(to)
            dest = dest + ".asp"

        if self.pargs.redirect_as != "skip":
            with open(dest, 'w') as f:
                f.write(content)

    def html_redirect(self, url, type_="html"):
        if type_ == 'html':
            rstr = """<meta http-equiv="Refresh" content="0; URL={url}" />"""
        else:
            rstr = """<script language="javascript" type="text/javascript">
    window.location.href="{url}";
</script>"""
        rstr = rstr.format(url=url)
        return """<html>
<head>
<title>Moved!</title>
{rstr}
</head>
<body>
<p>Page has moved: <a href="{url}">{url}</a></p>
</body>
</html>""".format(url=url, rstr=rstr)

    def php_redirect(self, url):
        return """<?php header("Location: {url}"); ?>"""\
                .format(url=url)

    def asp_redirect(self, url):
        return """<% Response.Redirect "{url}" %>"""\
                .format(url=url)


    def write_page(self, page, dest, menus):
        self.log.info("[PAGE] {}".format(page.url))
        try:
            menu = menus[page.language]

        except KeyError:
            menus[page.language] = [m.serialize() for m in
                                    Menu.get(self.app.mdb, page.language)]
            menu = menus[page.language]

        page_d = page.serialize()
        page_d['widgets'] = page.run_widgets(self.app.request)


        with open(dest, "wb") as f:
            response = render_to_response(page.template,
                                          dict(page=page_d, menus=menu),
                                          request=self.app.request)
            f.write(response.body)

        return menus

    @controller.expose()
    def default(self):
        outdir = os.path.realpath(self.pargs.outdir[0])
        self.log.info("Compiling pages to {}".format(outdir))
        pages = Page.all(self.app.mdb)
        menus = {}
        for page in pages:
            dest_file = os.path.join(outdir, page.url[1:])
            dest_dir = os.path.dirname(dest_file)
            try:
                os.makedirs(dest_dir)
                self.log.info("[MKDIR] {}".format(dest_dir))

            except OSError as e:
                if e.errno != 17:
                    raise

            if hasattr(page, "redirect"):
                self.write_redirect(from_=page.url, to=page.redirect['url'],
                                    dest=dest_file)

            else:
                menus = self.write_page(page, dest_file, menus)

        # handle homepage redirect
        home_name = "{}.html".format(self.pargs.index)
        home = os.path.join(outdir, home_name)
        lang = self.app.request.registry.settings['mokacms.default_language']
        if not os.path.exists(home):
            to = Page.homepage(self.app.mdb, lang)
            if to:
                self.write_redirect(from_="/" + home_name, to=page.url, dest=home)
