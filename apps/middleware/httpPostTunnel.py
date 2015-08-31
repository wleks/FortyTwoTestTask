# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import QueryDict


class HttpPostTunnelingMiddleware(object):
    def process_request(self, request):
        if 'HTTP_X_METHODOVERRIDE' in request.META:
            http_method = request.META['HTTP_X_METHODOVERRIDE']
            if http_method.lower() == 'put':
                request.method = 'PUT'
                request.META['REQUEST_METHOD'] = 'PUT'
                request.PUT = QueryDict(request.body)
        return None
