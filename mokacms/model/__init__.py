import logging
log = logging.getLogger(__name__)

from .page import Page
from .menu import Menu
from .theme import Theme

__all__ = ['Menu', 'Page', 'Theme', 'mongodb_start_request']


def mongodb_start_request(request):
    """Return the connection to the configured database.
       This function is called once per request as its return value
       is cached.
    """

    def cleanup(_):
        """ Callback handler for the "finished" request event """
        log.debug("Ending MongoDB request")
        request.registry.mongodb_connection.end_request()

    request.add_finished_callback(cleanup)
    request.registry.mongodb_connection.start_request()
    log.debug("Starting MongoDB request")
    return request.registry.mongodb_connection[request.registry.mongodb_database]


def init_model(database):
    """ Set up indexes on collections """
    log.info("init_model: creating indexes")
    database.themes.ensure_index("templates.file", unique=True)
    database.pages.ensure_index("url", unique=True)
    database.menus.ensure_index("name", unique=True)
