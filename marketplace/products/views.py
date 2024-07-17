from datetime import datetime

from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from catalog.serializers import CustomPagination
from products.models import Product, Tag, Review, Sale
from products.serializers import TagSerializers, ProductSerializers, ReviewSerializers, \
    ProductsPopularAndLimitedSerializers, SalesSerializers


class ProductDetail(RetrieveUpdateAPIView):
    """ Класс для получения подробной информации о деталях товара """
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

class ProductsPopular(APIView):
    """ Класс для получения последних 8 популярных товаров """
    def get(self, request: Request) -> Response:
        queryset = Product.objects.order_by("title", "id")[:8]
        serializer_class = ProductsPopularAndLimitedSerializers(queryset, many=True)
        return Response(serializer_class.data)

class ProductsLimited(APIView):
    """ Класс для получения последних 16 лимитированных товаров """
    def get(self, request: Request) -> Response:
        queryset = Product.objects.filter(limited=True)[:16]
        serializer_class = ProductsPopularAndLimitedSerializers(queryset, many=True)
        return Response(serializer_class.data)

class SalesAPIView(ListAPIView):
    """ Класс для получения скидок """
    queryset = Sale.objects.all()
    serializer_class = SalesSerializers
    pagination_class = CustomPagination

class BannersAPIView(APIView):
    """ Класс для получения баннера с 3 случайными товарами"""
    def get(self, request: Request) -> Response:
        queryset = Product.objects.order_by("?")[:3]
        serializer = ProductsPopularAndLimitedSerializers(queryset, many=True)
        return Response(serializer.data)

class TagsList(APIView):
    """ Класс для получения тегов """
    def get(self, request: Request) -> Response:
        tag = Tag.objects.all()
        serialized = TagSerializers(tag, many=True)
        return Response(serialized.data)

class ReviewCreate(CreateModelMixin, GenericAPIView):
    """ Класс для создания отзывов о товаре и расчета средней оценки о товаре """
    # serializer_class = ReviewSerializers
    permission_classes = [IsAuthenticated]
    def post(self, request: Request, pk: int) -> Response:
        product = Product.objects.get(pk=pk)
        Review.objects.create(
            author=request.data["author"],
            email=request.data["email"],
            text=request.data["text"],
            rate=request.data["rate"],
            #date=datetime.now(),
            products_id=product.pk,
        )
        review = [{
            "author": request.data["author"],
            "email": request.data["email"],
            "text": request.data["text"],
            "rate": request.data["rate"],
            "date": datetime.now()
        }]
        reviews = Review.objects.filter(products_id=product.pk)
        summa = sum([obj.rate for obj in reviews])
        product.rating = summa / len(reviews)
        product.save()
        return Response(review)