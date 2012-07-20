#!/usr/bin/env python

import os
import sys
from paste.deploy import loadapp

try:
    ini = os.environ['USERVE_PASTE_INI']
    f = open(ini)
    f.close()

except KeyError:
    sys.stderr.write("Missing ini\n")
    sys.stderr.flush()
    sys.exit(2)

except IOError:
    sys.stderr.write("{}: no such file or directory\n".format(ini))
    sys.stderr.flush()
    sys.exit(3)


os.environ['uWSGI_VHOST_MODE'] = '1'
application = loadapp("config:%s" % (os.environ['USERVE_PASTE_INI']))
del os.environ['USERVE_PASTE_INI']

