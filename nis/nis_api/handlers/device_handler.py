#!/usr/bin/env python

from nis_api.handlers.base_handler import BaseHandler
from nis_api.handlers.base_handler import NISapiException
from nis_api.models.device import Device
from nis_api.models.device import DeviceException
from nis_api.lib.load_list import LoadList
from bson.errors import InvalidId
import tornado.gen as gen


class DeviceHandler(BaseHandler):

    @gen.coroutine
    def get(self, params=""):
        try:
            if params:
                response = yield gen.Task(self.cb, LoadList.loadDevicesDict(
                        search_criteria={"device_id": int(params)}))
            elif self.args:
                response = yield gen.Task(self.cb, LoadList.loadDevicesDict(
                        search_criteria=self.args))
            else:
                response = yield gen.Task(self.cb, LoadList.loadDevicesDict())
           
            if response:
                if params: 
                    self.json_return(response[0])
                else:
                    self.json_return(response)
            else: 
                raise NISapiException("No data found.", 404)

        except (IndexError, InvalidId) as e:
            self.error = e
            self.json_return_error(str(e), 404)
        except DeviceException as e:
            self.error = e
            self.json_return_error(e.value, e.error)
        except NISapiException as e:
            self.error = e
            self.json_return_error(e.value, e.error)
        except Exception as e:
            self.error = e
            self.json_return_error(str(e), 500)
        finally:
            self.finish()

    @gen.coroutine
    def post(self):
        try:
            devices = []
            response = []

            if type(self.json_args) == dict:
                devices.append(self.json_args)
            elif type(self.json_args) == list:
                devices = self.json_args

            while len(devices):
                device = Device.from_dict(devices.pop())
                yield gen.Task(self.cb, device.create())
                response.append(device.to_dict())

            if len(response) == 1:
                response = response[0]

            self.json_return(response, 201)
        except NISapiException as e:
            self.error = e
            self.json_return_error(e.value, e.error)
        except DeviceException as e:
            self.error = e
            self.json_return_error(e.value, e.error)
        except Exception as e:
            self.error = e
            self.json_return_error(str(e), 500)
        finally:
            self.finish()
    
    @gen.coroutine
    def put(self, device_id=None):
        try:
            if device_id is None:
                raise NISapiException("Device id not provided.")

            device = yield gen.Task(self.cb,
                Device.from_device_id(device_id))

            for item in self.json_args:
                if item == "is_allocated":
                    if self.json_args[item] == True:
                        yield gen.Task(self.cb, device.allocate())
                    else:
                        yield gen.Task(self.cb, device.deallocate())
                elif item == "is_suspended":
                    if self.json_args[item] == True:
                        yield gen.Task(self.cb, device.suspend())
                    else:
                        yield gen.Task(self.cb, device.unsuspend())
                else:
                    raise NISapiException("Received non-mutable variable: {}".format(item))

            yield gen.Task(self.cb, device.apply(self.json_args))
            yield gen.Task(self.cb, device.update())
            self.json_return(device.to_dict())
        except NISapiException as e:
            self.error = e
            self.json_return_error(e.value, e.error)
        except Exception as e:
            self.error = e
            self.json_return_error(e.value, 500)
        finally:
            self.finish()

    @gen.coroutine
    def delete(self, device_id=None):
        try:
            if device_id is None:
                raise NISapiException("Must provide device_id.")

            yield gen.Task(self.cb, Device.delete(device_id))
            self.set_status(204)
        except NISapiException as e:
            self.error = e
            self.json_return_error(e.value, e.error)
        except DeviceException as e:
            self.error = e
            self.json_return_error(e.value, e.error)
        except Exception as e:
            self.error = e
            self.json_return_error(str(e), 500)
        finally:
            self.finish()
