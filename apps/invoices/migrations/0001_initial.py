# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invoice'
        db.create_table('invoices_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('packing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fulfilment.Packing'], unique=True)),
            ('signed_off', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('signed_off_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('signed_off_key', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('signed_off_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 20, 0, 0), null=True, blank=True)),
        ))
        db.send_create_signal('invoices', ['Invoice'])

        # Adding model 'InvoiceItem'
        db.create_table('invoices_invoiceitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invoices.Invoice'])),
            ('packing_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fulfilment.PackingItem'])),
            ('invoice_weight', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('invoice_quantity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('invoice_unit_weight', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('invoice_weight_price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('invoice_unit_price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('invoices', ['InvoiceItem'])


    def backwards(self, orm):
        # Deleting model 'Invoice'
        db.delete_table('invoices_invoice')

        # Deleting model 'InvoiceItem'
        db.delete_table('invoices_invoiceitem')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fulfilment.packing': {
            'Meta': {'object_name': 'Packing'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ordering.Order']", 'unique': 'True'})
        },
        'fulfilment.packingitem': {
            'Meta': {'ordering': "('order_item__sku',)", 'unique_together': "(('packing', 'order_item', 'procurement_item'),)", 'object_name': 'PackingItem'},
            'fulfilled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fulfilled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fulfilled_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'fulfilment_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fulfilment_unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fulfilment_unit_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fulfilment_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fulfilment_weight_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ordering.OrderItem']"}),
            'packing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fulfilment.Packing']"}),
            'packing_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'packing_unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'packing_unit_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'packing_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'packing_weight_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'procurement_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['procurement.ProcurementItem']"}),
            'substitue_product_variant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.ProductVariant']", 'null': 'True', 'blank': 'True'})
        },
        'invoices.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'packing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fulfilment.Packing']", 'unique': 'True'}),
            'signed_off': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'signed_off_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 20, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'signed_off_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'signed_off_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'invoices.invoiceitem': {
            'Meta': {'object_name': 'InvoiceItem'},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoices.Invoice']"}),
            'invoice_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_unit_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_weight_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'packing_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fulfilment.PackingItem']"})
        },
        'ordering.order': {
            'Meta': {'ordering': "['-opened']", 'object_name': 'Order'},
            'browser_ip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'buyer_accepts_marketing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'closed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fetched_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'financial_status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fulfillment_status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gateway': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landing_site': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'landing_site_ref': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'note_attributes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'opened': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'pushed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'referring_site': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shops.Shop']"}),
            'shopify_order_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'subtotal_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'synced_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'taxes_included': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'total_discounts': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_line_items_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_tax': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_weight': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'ordering.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'fulfillment_service': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fulfillment_status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'grams': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ordering.Order']"}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'requires_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shopify_order_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shopify_order_item_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shopify_product_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shopify_product_variant_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'variant_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'procurement.procurement': {
            'Meta': {'object_name': 'Procurement'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'procurement.procurementitem': {
            'Meta': {'object_name': 'ProcurementItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_unit_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_units': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'procured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'procured_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'procured_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'procurement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['procurement.Procurement']"}),
            'procurement_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'procurement_unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'procurement_unit_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'procurement_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'procurement_weight_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'product_variant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordered_product_variant'", 'to': "orm['products.ProductVariant']"}),
            'substitute_product_variant': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subtitute_product_variant'", 'null': 'True', 'to': "orm['products.ProductVariant']"})
        },
        'products.product': {
            'Meta': {'ordering': "['title']", 'object_name': 'Product'},
            'body_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fetched_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'pushed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shops.Shop']"}),
            'shopify_product_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'synced_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['taggit.Tag']", 'null': 'True', 'blank': 'True'}),
            'template_suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'products.productvariant': {
            'Meta': {'ordering': "['title']", 'object_name': 'ProductVariant'},
            'compare_at_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fetched_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fulfillment_service': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'grams': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory_management': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'inventory_policy': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'inventory_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'option1': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'option2': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'option3': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'pushed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'requires_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shopify_product_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shopify_product_variant_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'synced_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'taxable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
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
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['invoices']