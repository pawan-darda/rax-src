"""
    sphinxcontrib.autohttp.common
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The common functions for web framework reflection.

    :copyright: Copyright 2011 by Hong Minhee
    :license: BSD, see LICENSE for details.

"""

import builtins
from functools import reduce


def import_object(import_name):
    module_name, expr = import_name.split(':', 1)
    mod = __import__(module_name)
    mod = reduce(getattr, module_name.split('.')[1:], mod)
    globals = __builtin__
    if not isinstance(globals, dict):
        globals = globals.__dict__
    return eval(expr, globals, mod.__dict__)


def http_directive(method, path, content):
    method = method.lower().strip()
    if isinstance(content, str):
        content = content.splitlines()
    yield ''
    yield '.. http:{method}:: {path}'.format(**locals())
    yield ''
    for line in content:
        yield '   ' + line
    yield ''
