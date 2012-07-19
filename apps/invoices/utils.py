from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils import timezone

from invoices.models import Invoice, InvoiceItem
from fulfilment.models import Packing, PackingItem
from products.models import ProductVariant

import settings
import os.path

def process_packings(queryset):

    """
    Given a Packing and Packing Items that have been
    completed, process and generate Invoices
    """
    
    packings = queryset
    packing_count = 0
    
    for packing in packings:

        packing_items = PackingItem.objects.filter(packing=packing)
        
        invoice_kwargs = {
            'packing': packing,
            'signed_off_at': timezone.now(), }
            
        invoice = Invoice(**invoice_kwargs)
        invoice.save()
        try:
            print u'%s' % invoice
        except:
            pass

        packing_item_count = 0
        
        for packing_item in packing_items:
            if packing_item.fulfilled:
                invoice_item_kwargs = {
                    'invoice': invoice,
                    'packing_item': packing_item,
                    'invoice_weight': packing_item.fulfilment_weight,
                    'invoice_quantity': packing_item.fulfilment_quantity,
                    'invoice_unit_weight': packing_item.fulfilment_unit_weight,
                    'invoice_weight_price': packing_item.fulfilment_weight_price,
                    'invoice_unit_price': packing_item.fulfilment_unit_price,
                    'notes': packing_item.notes, }
                invoice_item = InvoiceItem(**invoice_item_kwargs)
                
                try:
                    invoice_item.full_clean()
                except ValidationError, e:
                    print e
                else:
                    invoice_item.save()
                    packing_item_count += 1
                    try:
                        print u'    %s' % invoice_item
                    except:
                        pass
            else:
                break

        if len(packing_items) == packing_item_count:
            packing_count += 1

    # Delete empty invoices
    if packing_count == 0 and invoice:
        invoice.delete()
    return packing_count
                
def create_invoices(queryset):
    
    """
    Given a set of Invoices create pdf versions
    for printing or email delivery
    """
    
    """
    VAGRoundedStd-Bold.otf
    VAGRoundedStd-Black.otf
    VAGRoundedStd-Light.otf
    VAGRoundedStd-Thin.otf
    """
    # FONTS
    
    import reportlab.rl_config 
    reportlab.rl_config.warnOnMissingFontGlyphs = 0 # we know some glyphs are missing, suppress warnings 
    
    folder = os.path.join(settings.STATIC_ROOT, "fonts")
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics 
    from reportlab.pdfbase.ttfonts import TTFont 
    pdfmetrics.registerFont(TTFont('VAGBold', os.path.join(folder, 'VAGRoundedStd-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('VAGBlack', os.path.join(folder, 'VAGRoundedStd-Black.ttf'))) 
    pdfmetrics.registerFont(TTFont('VAGLight', os.path.join(folder, 'VAGRoundedStd-Light.ttf'))) 
    pdfmetrics.registerFont(TTFont('VAGThin', os.path.join(folder, 'VAGRoundedStd-Thin.ttf')))
    
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Table, Image, TableStyle #SimpleDocTemplate, Paragraph, Spacer,
    
    import locale # for currency
    locale.setlocale(locale.LC_ALL, '' )
    
    invoices = queryset
    
    for invoice in invoices:
        
        filename = os.path.join(settings.MEDIA_ROOT, "invoices", invoice.packing.order.order_number + ".pdf")
        
        pdf = canvas.Canvas(
            filename,
            bottomup = 1)
        pdf.setPageSize((A4[1], A4[0]))
        
        # (841.88976377952747, 595.27559055118104)
        
        pdf.setFont('VAGBlack', 24)
        
        # Header
        pdf.drawString(40, 540, invoice.packing.order.shop.title)
        
        header_string = u'#%s - %s - %s' % (
            invoice.packing.order.order_number,
            invoice.packing.order.email,
            invoice.packing.order.billing_address)
        pdf.setFont('VAGLight', 14)
        pdf.drawRightString(800, 540, header_string)
        
        # Logo
        # logo_image = Image(
        #     "%s/images/wsp_logo.jpg" % settings.STATIC_ROOT,
        #     width=200,
        #     height=200) 
        # logo_image.drawOn(pdf, 100, 100)
        
        # Invoice Table
        invoice_data = [
            ['Q', 'Product', 'Weight', 'Kg Price', 'Price', 'Cost', 'Adjust'],]
        sub_total = 0.00
        invoice_data_rows = 1
        for invoice_item in invoice.invoiceitem_set.all():

            product_variant_kwargs = {
                'shopify_product_variant_id': invoice_item.packing_item.order_item.shopify_product_variant_id, }
            product_variant = ProductVariant.objects.get(**product_variant_kwargs)

            qty             = invoice_item.invoice_quantity if product_variant.option2 not in ['loose'] else None
            product         = invoice_item.packing_item.order_item.title
            kg              = round(float(invoice_item.invoice_weight), 3) / 1000.000 if invoice_item.invoice_weight else None
            price_per_kg    = locale.currency(invoice_item.invoice_weight_price) if invoice_item.invoice_weight_price else None
            price_per_item  = locale.currency(invoice_item.invoice_unit_price) if invoice_item.invoice_unit_price else None
            cost            = invoice_item.invoice_unit_price * invoice_item.invoice_quantity
            sub_total       += cost
            cost            = locale.currency(cost)
            invoice_data.append(
                [ qty, product, kg, price_per_kg, price_per_item, cost, ''] )
            invoice_data_rows += 1
        
        invoice_data_table = Table(
            invoice_data,
            colWidths=[40, 280, 80, 80, 80, 80, 120])
            
        invoice_data_table.setStyle(
            TableStyle([
                # All
                ('GRID', (0,0), (6,invoice_data_rows), 0.5, colors.grey),
                # Header
                ('FONT', (0,0), (-1,0), 'VAGBold', 10),
                ('ALIGNMENT', (0,0), (-1,0), 'CENTER'),
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                # Body
                ('ALIGNMENT', (0,0), (0,-1), 'CENTER'), # Quantity
                ('ALIGNMENT', (2,1), (5,-1), 'RIGHT'), # Numerical
                
                
                ]))
        
        w, h = invoice_data_table.wrapOn(pdf, 760, 400)
        invoice_data_table.drawOn(pdf, 40, 440 - h, 0)
        
        # Invoice Totals
        delivery_fee = 4.5
        invoice_total_data = [
            ['', 'Order Total', 'After Adjustments' ],
            ['Order', sub_total, '' ],
            ['Delivery', delivery_fee, ''],
            ['Sub-Total', sub_total + delivery_fee, ''],
        ]
        invoice_total_data.reverse()
        
        invoice_total_table = Table(
            invoice_total_data, 
            # style=[
            #     ('SPAN',(-1,-1),(-1,-3)), 
            # ]
        )
        
        # invoice_total_table.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.green),
        #                 ('TEXTCOLOR',(0,0),(1,-1),colors.red)])
        invoice_total_table.wrapOn(pdf,400,500)
        invoice_total_table.drawOn(pdf, 210, 200)

        pdf.showPage()
        pdf.save()
        