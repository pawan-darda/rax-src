#!/usr/bin/env python

import tornado
import pkgutil
import sys
from pkg_resources import resource_filename

from tornado.web import Application

# from nis_api.route import route
# from nis_api.handlers.page_not_found import NotFoundHandler


def load_all_modules_from_dir(dirname):
    """ This automatically loads all the modules in the given directory. """
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        if package_name not in sys.modules:
            module = importer.find_module(
                package_name).load_module(package_name)


def create_application(debug=False):
    """ create the tornado application """
    # To setup the routes automatically we need to import all the handlers
    load_all_modules_from_dir(resource_filename("nis_api", "handlers"))

    # routes = route.get_routes()
    # routes.append(tornado.web.url(r".*", NotFoundHandler))

    # application = Application(routes, debug=debug)
    # return application
