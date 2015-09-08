# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType


class Command(NoArgsCommand):
    help = "Whatch existing models and number of objects"

    def handle_noargs(self, **options):
        for mdl in ContentType.objects.all():
            mcl = mdl.model_class()
            msg = "%s:\t %s - %d" %\
                  (mcl.__module__, mcl.__name__, mcl._default_manager.count())
            self.stdout.write(msg)
            self.stderr.write("error:  %s" % msg)
