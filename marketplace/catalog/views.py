from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.filters import ProductFilter
from catalog.models import Categories
from catalog.serializers import CategoriesSerializers, CustomPagination
from products.models import Product, Review
from products.serializers import ProductSerializers


class CategoryAPIView(APIView):
    """ Класс для создания категорий товаров """
    def get(self, request: Request) -> Response:
        """ Функция для получения категорий товаров """
        category = Categories.objects.filter(parent__isnull=True)
        serialized = CategoriesSerializers(category, many=True)
        return Response(serialized.data)

class CatalogAPIView(ListAPIView):
    """ Класс для получения каталога товаров """
    serializer_class = ProductSerializers
    pagination_class = CustomPagination
    filterset_class = ProductFilter
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.request.query_params:
            name = self.request.query_params.get("filter[name]")
            minPrice = self.request.query_params.get("filter[minPrice]")
            maxPrice = self.request.query_params.get("filter[maxPrice]")
            freeDelivery = self.request.query_params.get("filter[freeDelivery]")
            available = self.request.query_params.get("filter[available]")
            tags = self.request.query_params.getlist('tags[]')
            category = self.request.META['HTTP_REFERER'].split('/')[4]
            if category:
                categories = [obj.pk for obj in Categories.objects.filter(parent_id=category)]
                categories.append(int(category))
                queryset = queryset.filter(category__in=categories)
            if name:
                queryset = queryset.filter(title__icontains=name)
            if minPrice:
                queryset = queryset.filter(price__gte=minPrice)
            if maxPrice:
                queryset = queryset.filter(price__lte=maxPrice)
            if freeDelivery and freeDelivery == "true":
                queryset = queryset.filter(freeDelivery=True)
            if available == "true":
                queryset = queryset.filter(available=True)
            if tags:
                queryset = queryset.filter(tags__in=tags)

            sort = self.request.query_params.get("sort")
            sortType = self.request.query_params.get("sortType")
            if sort == "price":
                if sortType == "inc":
                    queryset = queryset.order_by("-price")
                else:
                    queryset = queryset.order_by("price")
            elif sort == "rating":
                if sortType == "inc":
                    queryset = queryset.order_by("-rating")
                else:
                    queryset = queryset.order_by("rating")
            elif sort == "reviews":
                if sortType == "inc":
                    queryset = queryset.annotate(rev=Count("reviews")).order_by("-rev")
                    print(queryset)
                else:
                    queryset = queryset.annotate(rev=Count("reviews")).order_by("rev")
                    print(queryset)
            elif sort == "date":
                if sortType == "inc":
                    queryset = queryset.order_by("-date")
                else:
                    queryset = queryset.order_by("date")
            return queryset