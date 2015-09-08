# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import NoteModel


@receiver([post_save, post_delete],
          dispatch_uid='request_store')
def models_handler(sender, **kwargs):
    if sender._meta.app_label != 'hello':
        return
    if sender._meta.model_name == 'notemodel':
        return

    instance = kwargs.get('instance')
    created = kwargs.get('created')
    action_type = 2

    if created is not None:
        if created:
            action_type = 0
        else:
            action_type = 1

    note = NoteModel(model=sender.__name__,
                     inst=instance,
                     action_type=action_type)
    note.save()
