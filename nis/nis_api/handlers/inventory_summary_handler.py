 #!/usr/bin/env python
#dev: Seth Thomas
from nis_api.handlers.base_handler import BaseHandler
from nis_api.handlers.base_handler import NISapiException
from nis_api.lib.load_list import LoadList
import tornado.gen as gen

class InventorySummaryHandler(BaseHandler):

    @gen.coroutine    
    def get(self):
        try:
            if "is_allocated" not in self.args:
                self.args["is_allocated"] = False
            if "is_suspended" not in self.args:
                self.args["is_suspended"] = False

            results = yield gen.Task(self.cb, LoadList.loadSummary(search_criteria=self.args))

            if results:
                self.json_return(results, 200)
            else:
                raise NISapiException("No data found.", 404)

        except NISapiException as e:
            self.error = e
            self.json_return_error(e.value, e.error)      

        except Exception as e:
            self.error = e
            self.json_return_error(str(e), 500)
        finally:
            self.finish()

