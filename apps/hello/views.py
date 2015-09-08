# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse

import json

from .models import Person, RequestStore
from .decorators import not_record_request


def home_page(request):
    context = {}
    person = Person.objects.first()
    context['person'] = person
    if request.user.is_authenticated():
        RequestStore.objects.filter(new_request=1).update(new_request=0)
    return render(request, 'home.html', context)


@not_record_request
def request_view(request):
    return render(request, 'request.html')


@not_record_request
def request_ajax(request):
    if request.is_ajax():
        new_request = RequestStore.objects.filter(new_request=1).count()
        request_list = RequestStore.objects.all()[:10]
        list = serializers.serialize("json", request_list)
        data = json.dumps((new_request, list))
        return HttpResponse(data, content_type="application/json")

    return None
