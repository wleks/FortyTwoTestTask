# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from apps.hello.models import RequestStore


logger = logging.getLogger(__name__)


class RequestMiddle(object):
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        log_msg = '%s %s' % (request.method, request.path)

        if not getattr(view_func, 'not_record', False):
            req = RequestStore()
            req.path = request.path
            req.method = request.method

            existent_reg = RequestStore.objects\
                                       .filter(path=request.path).first()
            if existent_reg is not None:
                req.priority = existent_reg.priority

            if request.user.is_authenticated():
                req.user = request.user

            req.save()
            logger.info(log_msg + ' was saved')
        else:
            logger.info(log_msg + ' wasn\'t saved')

        return None
