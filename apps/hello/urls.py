# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'hello.views.home_page', name='home'),
)
