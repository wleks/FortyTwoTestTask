# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase

from datetime import date

from ..forms import PersonForm


class FormTest(TestCase):
    def test_form(self):
        """Test check form """
        form_data = {'name': '',
                     'surname': '',
                     'date_of_birth': None,
                     'email': ''}
        form = PersonForm(data=form_data)

        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['surname'], ['This field is required.'])
        self.assertEqual(form.errors['date_of_birth'],
                         ['This field is required.'])
        self.assertEqual(form.errors['email'], ['This field is required.'])

        form_data['email'] = 'woronowandex.ru'
        form = PersonForm(data=form_data)
        self.assertEqual(form.errors['email'],
                         ['Enter a valid email address.'])

        form_data['name'] = 'Aleks'
        form_data['surname'] = 'Woronow'
        form_data['date_of_birth'] = date(2015, 01, 02)
        form_data['email'] = 'woronow@yandex.ru'
        form = PersonForm(data=form_data)

        self.assertEqual(form.is_valid(), True)
