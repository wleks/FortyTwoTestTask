# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin


from .models import Person, RequestStore, NoteModel


admin.site.register(Person)
admin.site.register(RequestStore)
admin.site.register(NoteModel)
