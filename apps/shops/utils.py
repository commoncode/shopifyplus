from ordering.models import Order

from shopifyable.utils import parse_shop_objects

def fetch_orders(shops):
    
    for shop in shops:
        shop.orders()
        
        for _order in (shop._orders):
            
            orders = parse_shop_objects(shop, Order, _order)
    
    return orders