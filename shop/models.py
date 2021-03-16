from django.db import models
# from django.utils.translation import ugerttext_lazy
from django.contrib.auth.models import User

class Dish(models.Model):
    image = models.ImageField(upload_to='images/', null=True, verbose_name='Картинка',max_length=900)
    title = models.CharField(max_length=100, verbose_name='Название блюда')
    type = models.CharField(max_length=100, verbose_name='Тип блюда')
    description = models.CharField(max_length=500, verbose_name='Описание')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

class Drink(models.Model):
    image = models.ImageField(upload_to='images/', null=True, verbose_name='Картинка', max_length=900)
    title = models.CharField(max_length=100, verbose_name='Название напитка')
    type = models.CharField(max_length=100, verbose_name='Тип Напитка')
    description = models.CharField(max_length=500, verbose_name='Описание')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Напиток'
        verbose_name_plural = 'Напитки'


class Cart(models.Model):
    session_key = models.CharField(max_length=999, blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_cost = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)

    def get_total(self):
        items = CartContent.objects.filter(cart=self.id)
        total = 0
        for item in items:
            total += item.product.price * item.qty
        return total


class CartContent(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Dish, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(null=True)

