#!/usr/bin/env python

#import tornado.ioloop
from tornado.web import RequestHandler
from tornado.escape import json_encode
from tornado.escape import json_decode
from nis_api.config import config
from nis_api.models.device import DeviceValidator



class NISapiException(Exception):

    """
    Custom Exception for nisapi.

    """

    def __init__(self, value, error=400):
        self.value = value
        self.error = error

    def __str__(self):
        return str(self.value)


class BaseHandler(RequestHandler):

    args = {}
    json_args = {}
    PAGING_ENABLED = False
    index_page = None

    def prepare(self):
        self.args = self.get_args()
        content_type = self.request.headers.get("Content-Type")
        
        if self.request.method in ["POST", "PUT"]:
            if "application/json" in content_type and self.request.body:
                self.json_args = json_decode(self.request.body)
                if "data" in self.json_args:
                    self.json_args = self.json_args['data']
            else:
                self.json_return_error(
                    "Method Error: POST and PUT requests require "
                    "'Content-Type' = 'application/json' header and a data "
                    "payload body.")

    def get_current_user(self):
        return self.get_secure_cookie("seth")

    def get(self):
        if self.index_page is None:
            f = open('./index.html', 'r')
            self.index_page = f.read()

        self.write(self.index_page)

    def options(self, *args):
        pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods",
                        "GET, POST, DELETE, PUT, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")

    def json_return(self, response, status=200):
        try:
            if isinstance(response, dict):
                if '_id' in response:
                    del response['_id']
            elif isinstance(response, list):
                for each in response:
                    if '_id' in each:
                        del each['_id']
            
            self.set_header("Content-Type", "application/json")
            self.set_status(status)
            self.write(json_encode({"data": response}))

        except NISapiException as e: 
            self.json_return_error(e.value)
        except Exception as e:
            self.json_return_error(str(e))

    def json_return_error(self, response, status=400):
        self.set_header("Content-Type", "application/json")
        self.set_status(status)
        self.write(json_encode({"error": response}))

    def get_args(self):

        """
        Return a list of the arguments with the given name.

        If argument is not present, return an empty dict.

        """
        return DeviceValidator.parse_args(self.request.arguments)
    
    #Callback for all handlers 
    def cb(self, message, callback):
        callback(message)
