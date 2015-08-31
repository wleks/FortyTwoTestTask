# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings


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
    image = models.ImageField('photo',
                              blank=True,
                              null=True,
                              upload_to='photo/',
                              height_field='height',
                              width_field='width')
    height = models.PositiveIntegerField(default=1, null=True, blank=True)
    width = models.PositiveIntegerField(default=1,  null=True, blank=True)

    def gauge_height(self):
        width = 200
        ratio = float(self.height)/float(self.width)
        height = width*ratio
        size_photo = {'w': width, 'h': height}
        return size_photo

    def __unicode__(self):
        return '%s %s' % (self.surname, self.name)


class RequestStore(models.Model):
    path = models.CharField(max_length=250)
    method = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True,
                             null=True)
    date = models.DateTimeField(auto_now_add=True)
    new_request = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return "%s - %s" % (self.path, self.method)

    class Meta:
        ordering = ["-date"]
