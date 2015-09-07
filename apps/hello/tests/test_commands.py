# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO

from datetime import date

from ..models import Person


class CommandsTestCase(TestCase):
    def test_showmodels(self):
        """ Test showmodels command."""
        out = StringIO()
        call_command('showmodels', stdout=out, stderr=out)

        # check number of objects model Person is 0 
        self.assertIn('Person - 0', out.getvalue())
        self.assertIn('error:', out.getvalue())

        Person.objects.create(name='Ivan',
                              surname='Ivanov',
                              date_of_birth=date(2105, 7, 14),
                              email='hello@i.ua',
                              jabber='42cc@khavr.com')
        # number of objects model Person is 1, after person is created                        
        call_command('showmodels', stdout=out, stderr=out)
        self.assertIn('Person - 1', out.getvalue())
