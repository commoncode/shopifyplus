from ordering.models import Order
from products.models import Product

from shopifyable.utils import parse_shop_object

def fetch_orders(shops):

    orders = []
    for shop in shops:
        shop.orders(limit=250)

        for _order in (shop._orders):
            orders.append(parse_shop_object(shop, Order, _order))

    # Close orders that weren't fetched from the shopify server
    excluded = Order.objects.exclude(id__in=[order.id for order in orders])
    excluded.update(opened=False)

    # Open any orders that are closed that shouldn't be
    Order.objects.exclude(id__in=[order.id for order in excluded]).update(opened=True)

    return orders

def fetch_products(shops):

    products = []
    for shop in shops:

        shop.products()

        for _product in (shop._products):

            products.append(parse_shop_object(shop, Product, _product))

    return products
