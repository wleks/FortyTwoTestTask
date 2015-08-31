# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns(
    '',
    url(r'^$', 'hello.views.home_page', name='home'),
    url(r'^requests/$', 'hello.views.request_view', name='request'),
    url(r'^request_ajax/$', 'hello.views.request_ajax', name='request_ajax'),
    url(r'^add_contact/$', 'hello.views.form_page', name='form'),
    url(r'^add_contact/success/$',
        TemplateView.as_view(template_name="success.html"), name='success'),
)
