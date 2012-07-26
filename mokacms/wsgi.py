#!/usr/bin/env python

import os
import sys
import logging.config
from paste.deploy import loadapp
try:
    import uwsgi
    os.environ['uWSGI_VHOST_MODE'] = '1'

except ImportError:
    pass

try:
    ini = os.environ['USERVE_PASTE_INI']
    f = open(ini)

except KeyError:
    sys.stderr.write("Missing USERVE_PASTE_INI in environment\n")
    sys.stderr.flush()
    sys.exit(2)

except IOError:
    sys.stderr.write("{}: no such file or directory\n".format(ini))
    sys.stderr.flush()
    sys.exit(3)

else:
    f.close()
    del os.environ['USERVE_PASTE_INI']


logging.config.fileConfig(ini)
application = loadapp("config:%s" % (ini))
