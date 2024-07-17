from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from rest_framework.request import Request

from products.models import Product, ProductImage, Review, Tag, Sale, ProductSpecification

class ProductImageInline(admin.StackedInline):
    model = ProductImage

@admin.action(description="Archive products") # Указываем что данная функция является Action
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    """ Функция для отображения наличия продукта """
    queryset.update(archived=True) # Действие которое выполнит архивацию продуктов

@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    """ Функция для скрытия наличия продукта """
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Класс для управления товарами в админке """
    actions = [
        mark_archived,
        mark_unarchived,
    ]
    inlines = [
        ProductImageInline,
    ]
    list_display = "pk", "title", "price", "date", "category", "count", "description_short", "freeDelivery", \
        "rating", "available", "limited"
    list_display_links = "pk", "title"
    ordering = "-title", "pk"
    search_fields = "title", "price"
    fieldsets = [
        (None, {
            "fields": ("title", "count", "description", "category", "fullDescription")
        }),
        ("Price options", {
            "fields": ("price",)
        }),
        ("Extra_options", {
            "fields": ("available", "limited", "freeDelivery"),
            #"classes": ("collapse",),
            "description": "Extra options. File 'available' is for soft delete",
        })
    ]

    def get_queryset(self, request: Request):
        return Product.objects.prefetch_related("tag")

    def description_short(self, obj: Product) -> str:
        """ Функция отображает краткое описание товара """
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."

    # def tag_list(self, obj: Product) -> str:
    #     """ Функция возвращает список тегов """
    #     return ", ".join([b.name for b in obj.tag.all()])
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Класс для управления отзывами в админке """
    list_display = "id", "author", "email", "text", "rate", "date", "products"
    ordering = "id", "date"
    fieldsets = [
        (None, {
            "fields": ("author", "email", "text", "rate", "products")
        })
    ]
    search_fields = ["author", "email", "products"]

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """ Класс для управления скидками в админке """
    list_display = "id", "dateTo", "dateFrom", "salePrice", "product"
    ordering = "id", "dateTo", "dateFrom"
    fieldsets = [
        (None, {
            "fields": ("dateTo", "dateFrom", "salePrice", "product")
        })
    ]
    search_fields = ["product", ]

@admin.register(ProductSpecification)
class SpecificationAdmin(admin.ModelAdmin):
    """ Класс для управления характеристиками в админке """
    list_display = "id", "name", "value", "products"
    ordering = "id", "name", "products"
    fieldsets = [
        (None, {
            "fields": ("name", "value", "products")
        })
    ]
    search_fields = ["name", "products__title"]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Класс для управления тегами в админке """
    list_display = "id", "name", "products_list"
    ordering = "id", "name"
    fieldsets = [
        (None, {
            "fields": ("name", "products")
        })
    ]
    search_fields = ["name",]

    def products_list(self, obj):
        """ Функция возвращает список товаров """
        return ", ".join([b.title for b in obj.products.all()])