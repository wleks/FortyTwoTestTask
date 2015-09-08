# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser

from ..models import Person, RequestStore
from ..views import home_page
from test_models import get_temporary_image


class HomePageViewTest(TestCase):
    fixtures = ['_initial_data.json']

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

        self.client.get(reverse('contact:home'))
        request_store_count = RequestStore.objects.count()
        self.assertGreaterEqual(request_store_count, 1)

        # create 15 records to db yet
        req = RequestStore.objects.get(id=1)
        for i in range(1, 15):
            req.pk = None
            req.save()

        # check number of objects in db
        req_list = RequestStore.objects.count()
        self.assertEqual(req_list, i+1)

        # check that 10 objects in response
        response = self.client.get(reverse('contact:request_ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(10, response.content.count('pk'))
        self.assertEqual(10, response.content.count('GET'))


class FormPageTest(TestCase):
    fixtures = ['_initial_data.json']

    def setUp(self):
        self.person = Person.objects.first()

    def test_form_page_view(self):
        """
        Test check access to form page only authenticate
        users and it used template request.html.
        """

        # if user is not authenticate
        response = self.client.get(reverse('contact:form'))
        self.assertEqual(response.status_code, 302)

        # after authentication
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('contact:form'))
        self.assertTemplateUsed(response, 'form.html')

    def test_form_page_edit_data(self):
        """Test check edit data at form page."""

        self.client.login(username='admin', password='admin')

        # edit data by form page
        data = dict(name='Ivan', surname='Ivanov',
                    date_of_birth='2005-01-02',
                    bio='', email='ivanov@yandex.ru',
                    jabber='iv@jabb.com')

        response = self.client.post(reverse('contact:form'), data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        # data are shown at form page according to changed data
        self.assertNotIn(self.person.name, response.content)
        self.assertNotIn(self.person.surname, response.content)
        self.assertNotIn(self.person.date_of_birth.strftime('%Y-%m-%d'),
                         response.content)
        self.assertNotIn(self.person.email, response.content)
        self.assertNotIn(self.person.jabber, response.content)

        self.assertIn('Ivan', response.content)
        self.assertIn('Ivanov', response.content)
        self.assertIn('2005-01-0', response.content)
        self.assertIn('ivanov@yandex.ru', response.content)
        self.assertIn('iv@jabb.com', response.content)

        # check enter empty name and invalid data_of_birth, email
        data['name'] = ''
        data['date_of_birth'] = 200
        data['email'] = 'ivan@'

        response = self.client.post(reverse('contact:form'), data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)

        # response errors
        self.assertIn('This field is required.', response.content)
        self.assertIn('Enter a valid date.', response.content)
        self.assertIn('Enter a valid email address.', response.content)

        # data in db did not change
        edit_person = Person.objects.first()
        self.assertEqual('Ivan', edit_person.name)

    def test_form_page_upload_image(self):
        """Test check upload image file in form page."""

        data = dict(name='Ivan', surname='Ivanov',
                    date_of_birth='2005-01-02',
                    bio='', email='ivanov@yandex.ru',
                    jabber='iv@jabb.com',
                    image=get_temporary_image())

        self.client.login(username='admin', password='admin')

        # submitting test.jpg that was retuned get_temporary_image function
        self.client.post(reverse('contact:form'), data,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        person = Person.objects.first()
        # check that name of image file in db is test.jpg
        self.assertEqual('test.jpg', person.image.name.split('/')[-1])

        # delete test.jpg file
        person.delete()
