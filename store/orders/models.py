from django.contrib.auth.models import User
from django.db import models

from storeapp.models import *
# Create your models here.



class Order(models.Model):
    class Status(models.IntegerChoices):
        PAID = 1,'Оплачено'
        NOT_PAID = 0,'Не оплачено'

    first_name = models.CharField(max_length=50,verbose_name ="Имя")
    last_name = models.CharField(max_length=50,verbose_name ="Фамилия")
    email = models.EmailField()
    phone = models.IntegerField(verbose_name="Телефон")
    address = models.CharField(max_length=250,verbose_name ="Адресс")
    postal_code = models.CharField(max_length=20,verbose_name="Индекс")
    city = models.CharField(max_length=100,verbose_name="Город")
    created = models.DateTimeField(auto_now_add=True,verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True,verbose_name ="Обновлено")
    paid = models.BooleanField(choices=Status.choices,default=Status.NOT_PAID,verbose_name="Оплата")

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


    def __str__(self):
        return f'Order {self.id},{self.get_total_cost()}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f'{self.product},{self.price},{self.quantity}'

    def get_cost(self):
        return self.price * self.quantity