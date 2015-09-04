# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser

from ..models import Person, RequestStore
from ..views import home_page


class HomePageViewTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.person = Person.objects.first()

    def test_home_page_returns_correct_html(self):
        """Test check that home page returns correct html."""

        request = HttpRequest()
        request.user = AnonymousUser()
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
        request.user = AnonymousUser()
        response = home_page(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_view_content(self):
        """Test check content that show home page."""

        response = self.client.get(reverse('contact:home'))
        self.assertContains(response,
                            '<h1>42 Coffee Cups Test Assignmen</h1>',
                            html=True)
        self.assertContains(response, self.person.name)
        self.assertContains(response, self.person.surname)
        self.assertContains(response,
                            self.person.date_of_birth.strftime('%b. %d, %Y'))
        self.assertContains(response, self.person.email)
        self.assertContains(response, self.person.jabber)
        self.assertContains(response, self.person.bio[:10])
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

    def test_correct_show_image_home_page(self):
        """
        Test check correct edit data.
        """

        # size image in db
        self.assertEqual(self.person.height, 765)
        self.assertEqual(self.person.width, 1358)
        size_photo = self.person.gauge_height()

        # check that size image is shown at home page reduced
        response = self.client.get(reverse('contact:home'))
        self.assertNotContains(response, self.person.height)
        self.assertNotContains(response, self.person.width)
        self.assertContains(response, size_photo['h'])
        self.assertContains(response, size_photo['w'])


class RequestAjaxTest(TestCase):
    def test_request_ajax_view(self):
        """Test check that request_ajax view returns appropriate
           method, path and number of new_request by ajax
           when transition to home page: 'GET' and '/'
        """

        response = self.client.get(reverse('contact:home'))
        response = self.client.get(reverse('contact:request_ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('GET', response.content)
        self.assertIn('/', response.content)
        self.assertIn('1', response.content)


class RequestViewTest(TestCase):
    def test_request_view(self):
        """
        Test check access to request_view page
        and used template request.html.
        """

        response = self.client.get(reverse('contact:request'))

        self.assertTemplateUsed(response, 'request.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            '<h1>42 Coffee Cups Test Assignmen</h1>',
                            html=True)

    def test_request_ajax_content_empty_db(self):
        """
        Test check that request_ajax view returns
        empty response when transition to request_view page.
        """

        response = self.client.get(reverse('contact:request_ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # check that db is empty
        request_store_count = RequestStore.objects.count()
        self.assertGreaterEqual(request_store_count, 0)
        # check response is empty too
        self.assertIn('0', response.content)
        self.assertIn('[]', response.content)

    def test_request_ajax_content_record_db_more_10(self):
        """
        Test check that request_ajax view returns 10 objects
        when in db more than 10 records.
        """

        # create 15 records to db
        for i in range(1, 15):
            path = '/test%s' % i
            method = 'GET'
            RequestStore.objects.create(path=path, method=method)

        self.client.get(reverse('contact:home'))
        request_store_count = RequestStore.objects.count()
        self.assertGreaterEqual(request_store_count, 1)

        # check number of objects in db
        req_list = RequestStore.objects.count()
        self.assertEqual(req_list, i+1)

        # check that 10 objects in response
        response = self.client.get(reverse('contact:request_ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(10, response.content.count('pk'))
        self.assertEqual(10, response.content.count('GET'))
        self.assertNotIn('/test0', response.content)
        self.assertNotIn('/test5', response.content)
        self.assertIn('/test6', response.content)
        self.assertIn('/', response.content)


class FormPageTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.person = Person.objects.first()

    def test_form_page_view(self):
        """
        Test check access to form page only authenticate
        users and used template request.html.
        """

        # if user is not authenticate
        response = self.client.get(reverse('contact:form'))
        self.assertEqual(response.status_code, 302)

        # after authentication
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('contact:form'))
        self.assertTemplateUsed(response, 'form.html')
        self.assertIn(self.person.name, response.content)

    def test_form_page_edit_data(self):
        """
        Test check correct edit data.
        """

        # check that data are shown at form page according to db data
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('contact:form'))
        self.assertIn(self.person.name, response.content)
        self.assertIn(self.person.surname, response.content)

        # edit data by form page
        response = self.client.post(reverse('contact:form'),
                                    {'name': 'Ivan', 'surname': 'Ivanov'})
        # data are shown at form page according to changed data
        self.assertNotIn(self.person.name, response.content)
        self.assertNotIn(self.person.surname, response.content)
        self.assertIn('Ivan', response.content)
        self.assertIn('Ivanov', response.content)
