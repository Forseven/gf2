from django.test import TestCase
from django.test.client import Client

from authapp.models import ShopUser
from basketapp.models import Basket
from django.core.management import call_command

from mainapp.models import ProductCategory, Product


class BasketsTestCase(TestCase):
   def setUp(self):
       category = ProductCategory.objects.create(name="стулья")

       self.product_1 = Product.objects.create(name="стул 1",category=category,price = 1999.5,quantity=150)

       self.product_2 = Product.objects.create(name="стул 2",
                                          category=category,
                                          price=2998.1,
                                          quantity=125,
                                          is_active=False)

       self.product_3 = Product.objects.create(name="стул 3",
                                          category=category,
                                          price=998.1,
                                          quantity=115)
       self.user = ShopUser.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', age=33)
       new_basket_item = Basket(user=self.user, product=self.product_1)
       new_basket_item.quantity += 1
       new_basket_item.save()
       new_basket_item = Basket(user=self.user, product=self.product_2)
       new_basket_item.quantity += 1
       new_basket_item.save()
       new_basket_item = Basket(user=self.user, product=self.product_3)
       new_basket_item.quantity += 2
       new_basket_item.save()

   def test_basket_get(self):

       basket_items = Basket.objects.filter(user=self.user)
       product_0 = Product.objects.get(pk=basket_items[0].product_id)
       product_1 = Product.objects.get(pk=basket_items[1].product_id)
       product_2 = Product.objects.get(pk=basket_items[2].product_id)
       self.assertEqual(product_0, self.product_1)
       self.assertEqual(product_1, self.product_2)
       self.assertEqual(product_2, self.product_3)
