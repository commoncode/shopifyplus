# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Shop.shopify_domain'
        db.add_column('shops_shop', 'shopify_domain', self.gf('django.db.models.fields.CharField')(default='', max_length='256', blank=True), keep_default=False)

        # Adding field 'Shop.shopify_key'
        db.add_column('shops_shop', 'shopify_key', self.gf('django.db.models.fields.CharField')(default='', max_length='256', blank=True), keep_default=False)

        # Adding field 'Shop.shopify_secret'
        db.add_column('shops_shop', 'shopify_secret', self.gf('django.db.models.fields.CharField')(default='', max_length='256', blank=True), keep_default=False)

        # Adding field 'Shop.fetched_orders_at'
        db.add_column('shops_shop', 'fetched_orders_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Shop.shopify_domain'
        db.delete_column('shops_shop', 'shopify_domain')

        # Deleting field 'Shop.shopify_key'
        db.delete_column('shops_shop', 'shopify_key')

        # Deleting field 'Shop.shopify_secret'
        db.delete_column('shops_shop', 'shopify_secret')

        # Deleting field 'Shop.fetched_orders_at'
        db.delete_column('shops_shop', 'fetched_orders_at')


    models = {
        'shops.shop': {
            'Meta': {'object_name': 'Shop'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fetched_orders_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'host_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'shopify_domain': ('django.db.models.fields.CharField', [], {'max_length': "'256'", 'blank': 'True'}),
            'shopify_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shopify_key': ('django.db.models.fields.CharField', [], {'max_length': "'256'", 'blank': 'True'}),
            'shopify_secret': ('django.db.models.fields.CharField', [], {'max_length': "'256'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['shops']
