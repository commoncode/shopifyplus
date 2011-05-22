from django.core.exceptions import ValidationError, ObjectDoesNotExist

from invoices.models import Invoice, InvoiceItem
from fulfilment.models import Packing, PackingItem

import settings
import os.path

def process_packings(queryset):

    """
    Given a Packing and Packing Items that have been
    completed, process and generate Invoices
    """
    
    packings = queryset
    
    for packing in packings:
        
        packing_items = PackingItem.objects.filter(packing=packing)
        
        invoice_kwargs = {
            'packing': packing, }
            
        invoice = Invoice(**invoice_kwargs)
        invoice.save()
        print u'%s' % invoice
        
        for packing_item in packing_items:
            
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
                print u'    %s' % invoice_item
                
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
    
    from reportlab.pdfbase import pdfmetrics 
    from reportlab.pdfbase.ttfonts import TTFont 
    pdfmetrics.registerFont(TTFont('VAGBold', os.path.join(folder, 'VAGRoundedStd-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('VAGBlack', os.path.join(folder, 'VAGRoundedStd-Black.ttf'))) 
    pdfmetrics.registerFont(TTFont('VAGLight', os.path.join(folder, 'VAGRoundedStd-Light.ttf'))) 
    pdfmetrics.registerFont(TTFont('VAGThin', os.path.join(folder, 'VAGRoundedStd-Thin.ttf')))
    
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Table #SimpleDocTemplate, Paragraph, Spacer,
    
    invoices = queryset
    
    for invoice in invoices:
        
        filename = os.path.join(settings.MEDIA_ROOT, "invoices", invoice.packing.order.order_number + ".pdf")
        
        pdf = canvas.Canvas(
            filename,
            bottomup = 0)
        pdf.setFont('VAGBlack', 24)

        # Header
        pdf.drawString(100, 100, "Wholesale Plus Organics")
        
        header_string = u'#%s - %s - %s' % (
            invoice.packing.order.order_number,
            invoice.packing.order.email,
            invoice.packing.order.billing_address)
        pdf.setFont('VAGLight', 14)
        pdf.drawString(100, 150, header_string)
        
        # Invoice Table
        invoice_data = []
        sub_total = 0.00
        for invoice_item in invoice.invoiceitem_set.all():
            product         = invoice_item.packing_item.order_item.title
            qty             = invoice_item.invoice_quantity
            kg              = float(invoice_item.invoice_weight) / 1000.000 if invoice_item.invoice_weight else None
            price_per_kg    = invoice_item.invoice_weight_price
            price_per_item  = invoice_item.invoice_unit_price
            cost            = invoice_item.invoice_unit_price * float(invoice_item.invoice_quantity)
            sub_total       += cost
            invoice_data.append(
                [ qty, product, kg, price_per_kg, price_per_item, cost ] )
        
        invoice_data_table = Table(invoice_data)
        
        invoice_data_table.wrapOn(pdf,800,800)
        invoice_data_table.drawOn(pdf, 20, 300)
        
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
        invoice_total_table.wrapOn(pdf,400,500)
        invoice_total_table.drawOn(pdf, 210, 200)

        pdf.showPage()
        pdf.save()
        