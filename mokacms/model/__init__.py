import logging
from pymongo import Connection
log = logging.getLogger(__name__)


def mongodb_connect(request):
    """Return the connection to the configured database.
       This function is called once per request as its return value
       is cached.
    """
    conf = {s.replace("mongodb.", ""): request.registry.settings[s]
            for s in request.registry.settings
            if s.startswith("mongodb.") and "database" not in s}
    db = request.registry.settings["mongodb.database"]

    log.debug("Connection to mongodb: {}, database '{}'".format(conf, db))
    if "port" in conf:
        conf["port"] = int(conf["port"])

    conn = Connection(**conf)

    def cleanup(_):
        """ Callback handler for the "finished" request event """
        log.debug("Closing connection to mongodb '{}'".format(db))
        conn.close()

    request.add_finished_callback(cleanup)
    return conn[db]
