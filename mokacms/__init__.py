#!/usr/bin/env python
from pyramid.config import Configurator
import logging
import sys
import pymongo
from mokacms.model import init_model
log = logging.getLogger(__name__)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    includeme(config)
    config.scan("mokacms.views")
    return config.make_wsgi_app()


def get_api_prefix(settings):
    api_prefix = settings.get("mokacms.api.prefix", "/api")
    if not api_prefix.startswith("/"):
        api_prefix = "/{}".format(api_prefix)
    try:
        api_version = int(settings.get("mokacms.api.version", "1"))
        if api_version < 0:
            raise ValueError("API version must be >0")

    except ValueError as e:
        log.critical(str(e))
        sys.exit(10)

    pfx = "{}/v{}".format(api_prefix, api_version)
    log.info("Setting up API with prefix {}".format(pfx))
    return pfx


def add_routes(config, settings):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.registry.api_prefix = get_api_prefix(settings)
    config.add_route("api", config.registry.api_prefix)

    config.add_route("homepage", "/")
    config.add_route("favicon", "/favicon.ico")
    config.add_route("sitemap", "/sitemap.xml")
    config.add_route("robots", "robots.txt")
    config.add_route("page", "/*path")


def mongodb_connect(config, settings):
    conf = {s.replace("mongodb.", ""): settings[s]
            for s in settings
            if s.startswith("mongodb.") and "database" not in s}
    db = settings["mongodb.database"]

    log.info("Connection to mongodb: {}, database '{}'".format(conf, db))
    if "port" in conf:
        conf["port"] = int(conf["port"])

    # Override settings
    conf["auto_start_request"] = False

    config.registry.mongodb_settings = conf
    config.registry.mongodb_database = db
    try:
        config.registry.mongodb_connection = pymongo.Connection(**conf)

    except pymongo.errors.ConnectionFailure:
        log.exception("Cannot connect to MongoDB")
        sys.exit(11)

    config.set_request_property("mokacms.model.mongodb_start_request", 
                                name="mdb", reify=True)

    # Init model
    with config.registry.mongodb_connection.start_request():
        init_model(config.registry.mongodb_connection[db])


def includeme(config):
    settings = config.get_settings()
    mongodb_connect(config, settings)
    add_routes(config, settings)
