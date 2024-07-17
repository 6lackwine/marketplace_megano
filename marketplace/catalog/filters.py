from django_filters import rest_framework as filters

from products.models import Product

class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class ProductFilter(filters.FilterSet):
    """ Класс для фильтрации товаров """
    name = filters.CharFilter(field_name="title", lookup_expr="icontains")
    minPrice = filters.NumberFilter(field_name="price", lookup_expr="gte")
    maxPrice = filters.NumberFilter(field_name="price", lookup_expr="lte")
    freeDelivery = filters.BooleanFilter(field_name="freeDelivery")
    available = filters.BooleanFilter(field_name="available")
    tags = filters.CharFilter(field_name="tags", lookup_expr="in")
    class Meta:
        model = Product
        fields = ['title', 'price', "freeDelivery", "available", "tag"]