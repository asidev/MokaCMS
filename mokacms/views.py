
from pyramid.httpexceptions import (HTTPFound,
                                   HTTPNotFound)
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from mokacms.model import Page
import logging
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


@view_config(rout_name='page')
def serve_page(request):
    path = request.matchdict['path']
    page = Page.get(request.mdb, path)
    self.log.debug("found page: {}".format(page))
    if not page:
        return HTTPNotFound()
    try:
        return HTTPRedirection(code=page.redirect['code'],
                                    location=page.redirect['url'])
    except AttributeError:
        menus = Menu.get(request.mdb, default_lang)

        return render_to_response(page.template,
                          {'page': page.to_dict(),
                           'menus': [menu.to_dict() for menu in menus]},
                          request=request)


@view_config(route_name='sitemap', renderer='json')
def sitemap(request):
    return list(Page.all(request.mdb, raw=True))