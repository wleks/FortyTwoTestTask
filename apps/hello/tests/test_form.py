# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase

from datetime import date

from ..forms import PersonForm


class FormTest(TestCase):
    def test_form(self):
        """Test form"""
        form_data = {'name': '',
                     'surname': 'Woronow',
                     'date_of_birth': date(2105, 7, 14),
                     'email': 'aleks.woronow@yandex.ru',
                     'jabber': '42cc@khavr.com'}
        form = PersonForm(data=form_data)

        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors['name'], ['This field is required.'])

        form_data['name'] = 'Aleks'
        form = PersonForm(data=form_data)

        self.assertEqual(form.is_valid(), True)
