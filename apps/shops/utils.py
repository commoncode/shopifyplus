from ordering.models import Order
from products.models import Product

from shopifyable.utils import parse_shop_object

def fetch_orders(shops):
    
    orders = []
    for shop in shops:
        shop.orders()
        
        for _order in (shop._orders):
            
            # # import pdb; pdb.set_trace()
            # for oi in _order['line_items']:
            #     variant_id = oi['variant_id']
            #     print 'ID ::: %s' % variant_id
            #     if variant_id is None:
            #import ipdb; ipdb.set_trace()
            #         pass
            
            orders.append(parse_shop_object(shop, Order, _order))
    
    return orders
    
def fetch_products(shops):
    
    products = []
    for shop in shops:
        
        shop.products()
        
        for _product in (shop._products):
            
            products.append(parse_shop_object(shop, Product, _product))
            
    return products
