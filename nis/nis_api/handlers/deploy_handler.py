
#!/usr/bin/env python
#dev: Seth Thomas
from nis_api.handlers.base_handler import BaseHandler
from nis_api.handlers.base_handler import NISapiException
from nis_api.lib.load_list import LoadList, LoadListException
from nis_api.models.device import DeviceException
from nis_api.config import config
import tornado.gen as gen


class DeployHandler(BaseHandler):


    @classmethod
    def validate_deploy_payload(cls, payload):

        aggr_zone = payload.get('aggr_zone', None)
        if aggr_zone and not isinstance(aggr_zone, str):
            raise NISapiException("'aggr_zone' must be of type str.")

        dc = payload.get('dc')

        if not dc:
            raise NISapiException("'dc' is a required item.")

        if not isinstance(dc, str): 
            raise NISapiException("'dc' must be of type str.")

        if dc not in config.dcs:
            raise NISapiException("A valid dc is required.")

        if payload.get('devices'):
            if not isinstance(payload.get('devices'), list):
                raise NISapiException("'devices' must be a list.")

            devices_requested = payload.get('devices')[:]
            while(len(devices_requested) > 0):
                obj = devices_requested.pop()
                quantity = obj.get('quantity')
                product_id = obj.get('product_id')

                if obj in devices_requested: 
                    raise NISapiException("Duplicate items in payload. {}".format(obj))
                 
                if not quantity:
                    raise NISapiException(
                        "Must include the value 'quantity'.")
                
                if not isinstance(quantity, int):
                    raise NISapiException(
                        "'quantity' must be of type int.")
                
                if quantity < 1:
                    raise NISapiException(
                        "'quantity' must be a postive integer.")
                
                if not product_id:
                    raise NISapiException("'product_id' is a required item.")

                if not isinstance(product_id, str): 
                    raise NISapiException(
                        "'product_id' must be of type str.")

                if product_id not in config.product_map:
                    raise NISapiException(
                        "A product_id matching a currently registered "
                        "product is required.")
                           
        else: 
            raise NISapiException("No 'devices' in payload.")
                       
    @gen.coroutine
    def post(self):
        try: 
            if isinstance(self.json_args, list):
                if len(self.json_args) > 1:
                    raise NISapiException("Deploy does not accept multiple objects.")    
                elif len(self.json_args) == 1:
                    self.payload = self.json_args[0]
            else:
                self.payload = self.json_args

            """
                Validate the values being passed in
            """
            DeployHandler.validate_deploy_payload(self.payload)

            response = []
            all_devices = []
            attempts = 0
            success = False
            aggr_zone = None 
           
            """
                While we do not have a successful attempt or 
                we reach our maximum of 3 attempts, we will
                try to fetch devices to be deployed.
            """
            while (not success) and (attempts < 3):
                attempts += 1

                aggr_zone = self.payload.get('aggr_zone', None)
                dc = self.payload.get('dc')

                """
                fetch aggr zone (round robin or fill up single aggr)
                if nothing is returned, we throw an error as there is not
                enough inventory for that DC.

                """
                try:
                    if not aggr_zone:
                        aggr_zone = yield gen.Task(
                            self.cb,
                            LoadList.fetchAggrZone(payload=self.payload)
                    )
                  
                except LoadListException as e:
                    raise NISapiException(str(e))
                except Exception as e:
                    raise NISapiException(str(e))

                device_order = self.payload.get('devices')

                while(len(device_order) > 0):
                    obj = device_order.pop()

                    """
                        Set is_allocated to False in the obj, so
                        we don't pull devices that are already allocated.

                        cast product_id to int to be safe. 

                        fetch our devices based on quantity.

                    """
                    obj['is_allocated'] = False
                    obj['is_suspended'] = False
                    obj['aggr_zone'] = aggr_zone
                    obj['dc'] = dc
                    quantity = obj.pop('quantity', None)

                    device_list = yield gen.Task(
                        self.cb,
                        LoadList.loadDevices(search_criteria=obj,
                                             limit=int(quantity))
                    ) 

                    """
                        if no quantity is available, we raise an Exception.

                    """

                    if not device_list or len(device_list) < quantity:
                        raise NISapiException(
                            "Insufficient inventory for dc: {} and "
                            "product_id: {}".format(dc, obj.get('product_id')))

                    """
                    Grab only the device_id's and put into a list, for the response

                    append the device_list to all_devices, as this is a list of devices
                    that are istantiated. 

                    """
                    for x in device_list:
                        response.append({
                                          "device_type": x.device_type,
                                          "device_id": x.device_id,
                                          "core_template_id": x.core_template_id
                                        })
                        
                    all_devices += device_list
               
                """
                    Set device allocation on obtained devices and update
                    if device update fails a retry attempt will happen. 
                    3 total retries before error is sent. 
                """
                try:
                    #allocate devices in DB
                    for device in all_devices:
                        yield gen.Task(self.cb, device.allocate())
                        yield gen.Task(self.cb, device.update({"is_allocated": False}))
                        success = True
                    self.json_return(response)
                except Exception:
                    #rollback
                    for device in all_devices:
                        yield gen.Task(self.cb, device.deallocate())
                        yield gen.Task(self.cb, device.update())

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
