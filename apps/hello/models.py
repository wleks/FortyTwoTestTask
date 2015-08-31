# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Person(models.Model):
    name = models.CharField('name', max_length=250)
    surname = models.CharField('surname', max_length=250)
    date_of_birth = models.DateField('date of birth')
    bio = models.TextField('bio', blank=True)
    email = models.EmailField('email')
    jabber = models.EmailField('jabber', blank=True)
    skype_id = models.CharField('skype id',
                                blank=True,
                                max_length=250)
    other = models.TextField('other contact', blank=True)

    def __unicode__(self):
        return '%s %s' % (self.surname, self.name)
