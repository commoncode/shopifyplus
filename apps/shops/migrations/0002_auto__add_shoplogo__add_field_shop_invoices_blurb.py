# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'Shop.invoices_blurb'
        db.add_column('shops_shop', 'invoices_blurb',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # Deleting field 'Shop.invoices_blurb'
        db.delete_column('shops_shop', 'invoices_blurb')


    models = {
        'shops.shop': {
            'Meta': {'object_name': 'Shop'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'host_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoices_blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'shopify_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'shops.shoplogo': {
            'Meta': {'object_name': 'ShopLogo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shops.Shop']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['shops']