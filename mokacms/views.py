#!/usr/bin/env python
import logging
import os
from pyramid.httpexceptions import (HTTPFound,
                                   HTTPNotFound,
                                   HTTPRedirection)
from pyramid.renderers import render_to_response
from pyramid.response import FileResponse
from pyramid.view import view_config
from mokacms.model import (Page,
                           Menu)
log = logging.getLogger(__name__)


@view_config(route_name="api", renderer='json')
def api_test(request):
    db = request.mdb
    return {}


@view_config(route_name="homepage")
def default_homepage(request):
    default_lang = request.registry.settings['mokacms.default_language']
    log.debug("Redirecting to default language: /{}".format(default_lang))
    page = Page.homepage(request.mdb, default_lang)
    if not page:
        return HTTPNotFound()
    return HTTPFound(location=page.url)


@view_config(route_name='page')
def serve_page(request):
    path = "/" + "/".join(request.matchdict['path'])
    try:
        page = Page.get(request.mdb, path)

    except:
        return HTTPNotFound()

    log.debug("Found page: {}".format(page))
    try:
        return HTTPRedirection(code=page.redirect['code'],
                                    location=page.redirect['url'])
    except AttributeError:
        menus = Menu.get(request.mdb, page.language)
        page_d = page.asdict()
        page_d['widgets'] = page.run_widgets(request)
        log.debug("Rendering template %s", page.template)
        return render_to_response(page.template,
                          {'page': page_d,
                           'menus': [menu.asdict() for menu in menus]},
                          request=request)


@view_config(route_name='sitemap', renderer='sitemap.mako')
def sitemap(request):
    return dict(pages=Page.all(request.mdb))


@view_config(route_name='robots', renderer='robots.mako')
def robots(request):
    return dict()


@view_config(route_name='favicon')
def favicon(request):
    here = os.path.dirname(__file__)
    icon = os.path.join(here, 'static', 'favicon.ico')
    try:
        return FileResponse(icon, request=request)
    except OSError:
        return HTTPNotFound()
