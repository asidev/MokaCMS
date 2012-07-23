import logging
log = logging.getLogger(__name__)


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
