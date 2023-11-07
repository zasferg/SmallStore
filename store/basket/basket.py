from decimal import Decimal
from django.conf import settings
from storeapp.models import Product

class Basket(object):
    def __init__(self,request):

        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)

        if not basket :
            basket = self.session[settings.BASKET_SESSION_ID]  = {}

        self.basket = basket

    def add(self,product,quantity=1,update_quantity=False):
        product_slug = str(product.slug)
        if product_slug not in self.basket:
            self.basket[product_slug]={
                'quantity':0,
                'price':str(product.price)
            }
        if update_quantity:
            self.basket[product_slug]['quantity'] = quantity
        else:
            self.basket[product_slug]['quantity'] = quantity
        self.save()


    def save(self):
        self.session[settings.BASKET_SESSION_ID] = self.basket
        self.session.modified = True

    def remove(self,product):
        product_slug = str(product.slug)
        if product_slug in self.basket:
            del self.basket[product_slug]
            self.save()

    def __iter__(self):

        product_ids = self.basket.keys()

        products = Product.objects.filter(slug__in= product_ids)
        for product in products:
            self.basket[str(product.slug)]['product'] = product

        for item in self.basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price']*item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity']for item in self.basket.values())

    def get_total_price(self):

        return sum(Decimal(item['price'])*item['quantity'] for item in self.basket.values())


    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True