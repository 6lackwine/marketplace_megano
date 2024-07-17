from django.contrib import admin

from orders.models import Order, ProductOrderCount
from products.models import Product


class ProductOrderCountInline(admin.TabularInline):
    model = ProductOrderCount

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Класс для управления заказами в админке """
    inlines = [
        ProductOrderCountInline,
    ]
    list_display = "id", "user", "createdAt", "fullName", "email", "phone", "deliveryType",\
        "paymentType", "totalCost", "status", "city", "address", "products_list"
    fieldsets = [
        (None, {
            "fields": ("user", "fullName", "email", "phone", "deliveryType",
                       "paymentType", "totalCost", "status", "city", "address")
        }),
    ]
    search_fields = ["id", "user__user__username", "fullName", "phone", "status", "city", "address"]
    list_per_page = 10

    def products_list(self, obj: ProductOrderCount):
        """ Функция возвращает список товаров в заказе """
        return ", ".join([b.title for b in obj.products.all()])

    # def products_list(self, obj: Order):
    #     return ", ".join([product.title for product in obj.products.all()])


@admin.register(ProductOrderCount)
class ProductOrderCountAdmin(admin.ModelAdmin):
    """ Класс для управления количеством продуктов в заказе в админке """
    list_display = "id", "order", "products", "count"
    ordering = ["order"]
    fieldsets = [
        (None, {
            "fields": ("order", "products", "count")
        })
    ]

    # def products_list(self, obj: ProductOrderCount):
    #     return ", ".join([p.title for p in obj.order.products.all()])
