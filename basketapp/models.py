from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.utils.functional import cached_property

class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    def get_items(user):
        return Basket.objects.filter(user=user)


    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @staticmethod
    def get_product(user,product):
        return Basket.objects.filter(user=user,product=product).first()

    def get_total_quantity(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    def get_total_cost(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))

    def _get_product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity
    
    product_cost = property(_get_product_cost)
    

    def _get_total_quantity(self):
        "return total quantity for user"
        _items = Basket.objects.filter(user=self.user)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    total_quantity = property(_get_total_quantity)


    def _get_total_cost(self):
        "return total cost for user"
        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    total_cost = property(_get_total_cost)
