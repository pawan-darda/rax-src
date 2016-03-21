#!/usr/bin/env python
import datetime
from pymongo import MongoClient

class Config(object):

    mongo = {
        'db': 'nis',
        'host': 'localhost',
        'port': 27017,
        'user': 'nis',
        'pass': '',
        'enable_auth': False
    }

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """ Configuration Object """
        self.version = '1.0'
        self.debug_mode = False
        self.admin_enabled = False

        # True - aggr with most devices is picked (this is to balance the aggrs)
        # False - aggr with least devices is picked, until empty
        self.aggr_round_robin = self.get_round_robin()
        if not self.aggr_round_robin:
            self.update_admin(True)

        self.date = datetime.datetime.now()
        self.log = "/var/log/nis_api.log"
        self.log_error = "/var/log/nis_api_error.log"
        self.log_alerts = "/var/log/nis_api_alert.log"

        self.tornado = {
            'port': 8080
        }

        self.CTK_CONFIG = {
             'user': 'user',
             'password': 'password',
             'environment': 'staging'
         }

         self.HOLDING_ACCOUNTS = [1823864, 2991798]

        self.dcs = {
            "AMS1": 12,
            "AUS1": 9,
            "AUS2": 29,
            "BCB1": 17,
            "CDC1": 26,
            "CVG1": 30,
            "DFW1": 5,
            "DFW2": 25,
            "GER1": 16,
            "HKG1": 14,
            "HKO1": 23,
            "IAD1": 4,
            "IAD2": 21,
            "IAD3": 32,
            "LON1": 2,
            "LON2": 7,
            "LON3": 13,
            "LON4": 24,
            "LONB": 8,
            "ORD1": 22,
            "SAT1": 1,
            "SAT2": 3,
            "SAT4": 6,
            "SAT6": 15,
            "STO1": 10,
            "STO2": 11,
            "SYD1": 27,
            "SYD2": 31,
            "TST1": 33,
            "TST2": 34,
            "ZRH1": 28,
        }
        self.update_product_map()

    ## Add swapped key/values for reverse lookups
    # datacenter.update({v: k for k, v in datacenter.items()})

    @classmethod
    def get_db_collection(cls, collection):
        client = MongoClient(cls.mongo['host'], cls.mongo['port'])
        db = client[cls.mongo['db']]
        if cls.mongo['enable_auth']:
            db.authenticate(cls.mongo['user'], cls.mongo['pass'])
        return db[collection]

    @classmethod
    def get_products(cls):
        product_collection = cls.get_db_collection('products')
        return product_collection.find({})

    def update_product_map(self):
        self.product_map = {}
        for x in Config.get_products():
            self.product_map[x.get('product_id')] = {
                'product_name': x.get('product_name'),
                'device_type': x.get('device_type')}
        return self.product_map

    def get_round_robin(self):
        collection = Config.get_db_collection('admin')
        t = collection.find_one({"admin": "admin"})
        if t:
            return t.get("aggr_round_robin")

    def update_admin(self, aggr_round_robin):
        collection = Config.get_db_collection('admin')
        if collection.find_one({"admin": "admin"}):
            collection.update(
                {"admin": "admin"},
                {"admin": "admin", "aggr_round_robin": aggr_round_robin})
        else:
            collection.insert(
                {"admin": "admin", "aggr_round_robin": aggr_round_robin})
        self.aggr_round_robin = aggr_round_robin

config = Config()