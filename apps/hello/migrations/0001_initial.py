# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'hello_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('jabber', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('skype_id', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('other', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'hello', ['Person'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'hello_person')


    models = {
        u'hello.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'other': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'skype_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['hello']