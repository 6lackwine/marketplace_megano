from django.db import models

from products.models import Product
from profiles.models import Profiles


class Order(models.Model):
    """ Класс для создания модели заказа """
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE, verbose_name="Пользователь")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    fullName = models.CharField(max_length=100, verbose_name="Фамилия Имя Отчество")
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    deliveryType = models.CharField(max_length=100, verbose_name="Способ доставки")
    paymentType = models.CharField(max_length=100, verbose_name="Способ оплаты")
    totalCost = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    status = models.CharField(max_length=100, verbose_name="Статус")
    city = models.CharField(max_length=100, blank=True, verbose_name="Город")
    address = models.CharField(max_length=100, blank=True, verbose_name="Адрес")
    products = models.ManyToManyField(Product, related_name="orders", verbose_name="Товары", through="ProductOrderCount")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.pk}"

class ProductOrderCount(models.Model):
    """ Класс для создания модели подсчета товаров и их количества в корзине """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товары")
    count = models.PositiveIntegerField(verbose_name="Количество", null=True)

    class Meta:
        verbose_name = "Товар и его количество"
        verbose_name_plural = "Товары и их количество"

    def __str__(self):
        return f"{self.products}"