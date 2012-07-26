#!/usr/bin/env python
import json
import os
import sys
from cement.core import controller
from . base import MokaBaseController
import mokacms.model

class MokaDatabaseController(MokaBaseController):
    class Meta:
        label = 'database'
        description = 'Manage database-related stuff'
        arguments = [
            (['-d', '--datafile'],
              dict(help="database data file",
                   default="data.json")),
            (['-k', '--keep', '--keep-collections'],
             dict(action="store_true",
                  help="do not empty collections",
                  default=False))
        ]

    @controller.expose()
    def setup(self):
        datafile = self.pargs.datafile
        close = False
        try:
            if datafile == '-':
                data_obj = sys.stdin
                self.log.info("Loading JSON data from stdin")

            else:
                if not datafile.startswith('/'):
                    datafile = os.path.join(self.app.root_path, "data",
                                            datafile)
                datafile = os.path.realpath(datafile)
                self.log.info("Loading JSON data from {}".format(datafile))
                data_obj = open(datafile)
                close = True

        except (ValueError, IOError) as e:
            self.log.error(str(e))

        else:
            data = json.load(data_obj)
            self.log.debug("Read JSON data:")
            self.log.debug(data)

            for collection_name, info in data.items():
                self.log.info("Importing data for collection '{}'"\
                              .format(collection_name))

                collection = getattr(self.app.mdb, collection_name)
                cls = getattr(mokacms.model, collection_name.title()[:-1])

                if not self.pargs.keep:
                    collection.remove({})

                for elem in info:
                    obj = cls(elem)
                    obj.save(self.app.mdb)

            self.log.info("Done")
            self.result = dict(success=True)

        finally:
            if close:
                data_obj.close()
