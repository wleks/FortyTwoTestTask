# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps


def not_record_request(func=None):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        return func(request, *args, **kwargs)
    wrapped.not_record = True
    return wrapped
