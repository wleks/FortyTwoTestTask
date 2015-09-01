# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.http import HttpRequest

from ..models import Person
from ..views import home_page


class HomePageViewTest(TestCase):
    fixtures = ['_initial_data.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.person = Person.objects.first()

    def test_home_page_returns_correct_html(self):
        """Test check that home page returns correct html."""

        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.strip().
                        startswith(b'<!DOCTYPE html>'))
        self.assertIn(b'<title>Visiting Card</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))

    def test_home_page_view(self):
        """
        Test check access to home page
        and used template home.html
        """

        request = self.factory.get(reverse('contact:home'))
        response = home_page(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_view_content(self):
        """Test check content that show home page."""

        response = self.client.get(reverse('contact:home'))
        self.assertContains(response,
                            '<h1>42 Coffee Cups Test Assignmen</h1>',
                            html=True)
        self.assertContains(response, 'Aleks')
        self.assertContains(response, 'Woronow')
        self.assertContains(response, 'Aug. 22, 2015')
        self.assertContains(response, 'aleks.woronow@yandex.ru')
        self.assertContains(response, 'aleksw@42cc.com')
        self.assertContains(response, 'I was born ...')
        self.assertEqual(self.person, response.context['person'])

    def test_home_page_empty_db(self):
        """Test check that person db is empty
           home page is empty as well
        """

        Person.objects.all().delete()
        response = self.client.get(reverse('contact:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            '<li class="list-group-item">Email:</li>',
                            html=True)

    def test_home_page_two_records_person_db(self):
        """Test check that person db has two records
           home page show only first
        """

        Person.objects.create(name='Иван',
                              surname='Иванов',
                              bio='',
                              email='iv@i.ua',
                              jabber='iv@khavr.com',
                              skype_id='',
                              date_of_birth='2000-01-01',
                              other='')

        p = Person.objects.count()
        first = Person.objects.first()

        self.assertGreaterEqual(p, 2)

        response = self.client.get(reverse('contact:home'))
        self.assertEqual(first, response.context['person'])

        self.assertContains(response, 'Aleks')
        self.assertContains(response, 'Woronow')
        self.assertContains(response, 'Aug. 22, 2015')
        self.assertContains(response, 'aleks.woronow@yandex.ru')
        self.assertContains(response, 'aleksw@42cc.com')
        self.assertContains(response, 'I was born ...')

        self.assertNotContains(response, 'Иван')
        self.assertNotContains(response, 'Иванов')
        self.assertNotContains(response, 'Jun. 01, 2000')
        self.assertNotContains(response, 'iv@i.ua')
        self.assertNotContains(response, 'iv@khavr.com')
