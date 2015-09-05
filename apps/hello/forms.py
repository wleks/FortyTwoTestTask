# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import ModelForm
from django import forms

from .models import Person


class CalendarWidget(forms.DateInput):
    class Media:
        js = ('http://code.jquery.com/ui/1.11.0/jquery-ui.js',)

    def __init__(self, attrs={}):
        super(CalendarWidget, self).__init__(
            attrs={'class': 'form-control datepicker', 'size': '10'})


class PersonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'image' and field_name != 'date_of_birth':
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Person
        fields = ['name', 'surname', 'date_of_birth', 'bio',
                  'email', 'jabber', 'skype_id', 'other', 'image']
        widgets = {
            'date_of_birth': CalendarWidget(),
            'image': forms.FileInput()
        }

    class Media:
        js = ('js/change_person_data.js',)
