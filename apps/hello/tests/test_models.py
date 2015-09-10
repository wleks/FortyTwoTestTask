# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse

from datetime import date
from PIL import Image as Img
import StringIO

from ..models import Person, NoteModel, RequestStore


# create image file for test
def get_temporary_image():
        output = StringIO.StringIO()
        size = (1200, 700)
        color = (255, 0, 0, 0)
        image = Img.new("RGBA", size, color)
        image.save(output, format='JPEG')
        image_file = InMemoryUploadedFile(output,
                                          None,
                                          'test.jpg',
                                          'jpeg',
                                          output.len,
                                          None)
        image_file.seek(0)
        return image_file


class PersonModelTests(TestCase):
    fixtures = ['_initial_data.json']

    def test_person_model(self):
        """Test creating a new person and saving it to the database"""
        person = Person()

        # test model blank and null fields validation
        with self.assertRaises(ValidationError) as err:
            person.full_clean()
        err_dict = err.exception.message_dict
        self.assertEquals(err_dict['name'][0],
                          Person._meta.get_field('name').
                          error_messages['blank'])
        self.assertEquals(err_dict['surname'][0],
                          Person._meta.get_field('surname').
                          error_messages['blank'])
        self.assertEquals(err_dict['email'][0],
                          Person._meta.get_field('email').
                          error_messages['blank'])
        self.assertEquals(err_dict['date_of_birth'][0],
                          Person._meta.get_field('date_of_birth').
                          error_messages['null'])

        # test model email and date field validation
        person.email = 'aleks@'
        person.jabber = '42cc'
        person.date_of_birth = 'sd'
        with self.assertRaises(ValidationError) as err:
            person.full_clean()
        err_dict = err.exception.message_dict
        self.assertEquals(err_dict['email'][0],
                          EmailValidator.message)
        self.assertEquals(err_dict['jabber'][0],
                          EmailValidator.message)
        self.assertIn(Person._meta.get_field('date_of_birth').
                      error_messages['invalid'].format()[12:],
                      err_dict['date_of_birth'][0])

        # test cretae and save object
        person.name = 'Aleks'
        person.surname = 'Woronow'
        person.date_of_birth = date(2105, 7, 14)
        person.bio = 'I was born ...'
        person.email = 'aleks.woronow@yandex.ru'
        person.jabber = '42cc@khavr.com'
        person.skype_id = ''
        person.other = ''

        # check we can save it to the database
        person.save()

        # now check we can find it in the database again
        all_persons = Person.objects.all()
        self.assertEquals(len(all_persons), 2)
        only_person = all_persons[1]
        self.assertEquals(only_person, person)

        # and check that it's saved its two attributes: name and surname
        self.assertEquals(only_person.name, 'Aleks')
        self.assertEquals(only_person.surname, 'Woronow')
        self.assertEquals(only_person.bio, 'I was born ...')
        self.assertEquals(str(only_person), 'Woronow Aleks')

    def test_person_model_image(self):
        """
        Test check that overwritten save method maintaining aspect ratio
        and reduce image to <= 200*200.
        """

        # save image file
        person = Person.objects.get(id=1)
        person.image = get_temporary_image()
        person.save()

        # check that height and width <= 200
        self.assertTrue(person.height <= 200)
        self.assertTrue(person.width <= 200)

        person.delete()


class NoteModelTestCase(TestCase):
    fixtures = ['test_data.json']

    def test_signal_processor(self):
        """
        Test signal processor records create,
        change and delete object.
        """
        # check action_type after created object (loaded fixtures) is 0
        note = NoteModel.objects.get(model='Person')
        self.assertEqual(note.action_type, 0)

        # check action_type after change object is 1
        person = Person.objects.first()
        person.name = 'Change'
        person.save()
        note = NoteModel.objects.filter(model='Person').last()
        self.assertEqual(note.action_type, 1)

        # check record after delete object is 2
        person = Person.objects.first()
        person.delete()
        note = NoteModel.objects.last()
        self.assertEqual(note.action_type, 2)


class RequestModelTestCase(TestCase):
    def test_record_priority_field(self):
        """
        Test record priority field.
        """

        # pass to home page
        self.client.get(reverse('contact:home'))
        request_store = RequestStore.objects.first()

        # check record RequestStore contains:
        # method - 'GET' and default priority - 0
        self.assertEqual(request_store.path, '/')
        self.assertEqual(request_store.method, 'GET')
        self.assertEqual(request_store.priority, 0)

        # change priority to 1 and send POST to home page
        request_store.priority = 1
        request_store.save()
        self.client.post(reverse('contact:home'))

        # check record RequestStore contains:
        # method - 'POST' and default priority - 1
        request_store = RequestStore.objects.first()
        self.assertEqual(request_store.method, 'POST')
        self.assertEqual(request_store.priority, 1)
