from rest_framework import serializers, pagination
from rest_framework.response import Response

from catalog.models import Categories, CategoryImage
from products.models import Product


class CategoryImageSerializers(serializers.ModelSerializer):
    """ Класс для сериализации изображения категорий товаров"""
    class Meta:
        model = CategoryImage
        fields = "src", "alt"

class SubcategoriesSerializers(serializers.ModelSerializer):
    """ Класс для сериализации подкатегорий товаров """
    image = CategoryImageSerializers()
    class Meta:
        model = Categories
        fields = "id", "title", "image"

class CategoriesSerializers(serializers.ModelSerializer):
    """ Класс для сериализации категорий товаров """
    title = serializers.CharField(max_length=100)
    image = CategoryImageSerializers()
    subcategories = SubcategoriesSerializers(many=True)
    # subcategories = serializers.SerializerMethodField()

    # def get_subcategories(self, obj):
    #     queryset = Categories.objects.filter(subcategories=obj)
    #     if obj.subcategories is None:
    #         return [CategoriesSerializers(q).data for q in queryset]
    #     return CategoriesSerializers(queryset, many=True).data
    class Meta:
        model = Categories
        fields = "id", "title", "image", "subcategories"

class BasketSerializers(serializers.ModelSerializer):
    """ Класс для сериализации корзины товаров """
    class Meta:
        model = Product
        fields = "id", "category", "price", "count", "date", "title", "description", \
            "freeDelivery", "images", "tags", "reviews", "rating"

class CustomPagination(pagination.PageNumberPagination):
    """ Класс для создания пагинации в каталоге товаров """
    page_size = 5
    max_page_size = 1000
    page_query_param = "currentPage"
    def get_paginated_response(self, data: dict) -> Response:
        """ Функция для получения пагинации """
        return Response({
            'items': data,
            "currentPage": self.page.number, #self.request.query_params["currentPage"],
            "lastPage": self.page.paginator.num_pages,
        })