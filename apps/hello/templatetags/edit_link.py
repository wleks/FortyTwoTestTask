# -*- coding: utf-8 -*-
from django import template
from django.db import models
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.inclusion_tag('templatetags/edit_link.html')
def edit_link(obj):
    if isinstance(obj, models.Model):
        model = ContentType.objects.get_for_model(obj)
        edit_link = '/admin/%s/%s/%d' %\
                    (model.app_label, model.model, int(obj.id))
        return {
            'edit_link': edit_link,
            'model': model.model,
        }

    return None
