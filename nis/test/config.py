#!/usr/bin/env python
import datetime
from pymongo import MongoClient


class Config:

    """ Configuration Object """
    version = '1.0'

    admins = ['seth.thomas@rackspace.com', 'fernando.pena@rackspace.com']

    paging = {
        'skip': 0,
        'limit': 25
    }

    ## Core Consumer
    #core_holding_account = 11
    #core_throttle = 5

    ## CtkCommander
    #ctk_api = {
    #    'url': 'https://staging.core.rackspace.com/ctkapi/',
    #    'username': 'melissa.biles',
    #    'password': 'qwerty',
    #    'token': ''
    #}

    date = datetime.datetime.now()
    log = 'log/rad_api_%d-%d-%d.log' % (
        date.month, date.day, date.year)
    log_error = 'log/rad_api_error_%d-%d-%d.log' % (
        date.month, date.day, date.year)
    log_alerts = 'log/rad_api_alerts_%d-%d-%d.log' % (
        date.month, date.day, date.year)

    mongo = {
        'db': 'rad',
        'host': '10.23.246.87',  # dev.rad.encore.rackspace.com
        'port': 27017
    }

    #mq = {
    #    'enabled': True,
    #    #'url': 'mq.core.rackspace.com:5671',
    #    'url': 'mq.staging.core.rackspace.com:5671',
    #    'vhost': 'core',
    #    'account': str(core_holding_account),
    #    'complete_status': 9  # 'Segment Configuration'
    #}

    email = {
        'server': '10.12.120.19',
        'from': 'encore_devices@rackspace.com',
        'user': 'encore_devices',
        'pass': 'zVV=e7ya(s4U3P}x'
    }

    tornado = {
        'port': 8080
    }

    datacenter = {
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

    flavor_map = {
        123456: "Flavor One",
        234567: "Flavor Two",
        345678: "Flavor Three"
    }

    ## Add swapped key/values for reverse lookups
    # datacenter.update({v: k for k, v in datacenter.items()})

    @classmethod
    def get_db_collection(cls, collection):
        client = MongoClient(cls.mongo['host'], cls.mongo['port'])
        return client[cls.mongo['db']][collection]

config = Config()
