# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import ModelForm

from .models import Person


class PersonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'date_of_birth':
                field.widget.attrs['class'] = 'form-control datepicker'
            else:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Person
        fields = ['name', 'surname', 'date_of_birth', 'bio',
                  'email', 'jabber', 'skype_id', 'other']

    class Media:
        js = ('js/change_person.js',)
