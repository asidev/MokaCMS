from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    includeme(config)
    config.scan()

    return config.make_wsgi_app()

def add_routes(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

def includeme(config):
    config.set_request_property("mokacms.model.mongodb_connect", name="mdb",
                                reify=True)
    add_routes(config)
