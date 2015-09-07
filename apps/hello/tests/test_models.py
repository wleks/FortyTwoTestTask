# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.files.uploadedfile import InMemoryUploadedFile

from datetime import date
from PIL import Image as Img
import StringIO

from ..models import Person


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
