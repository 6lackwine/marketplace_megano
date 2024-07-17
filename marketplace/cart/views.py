import json

from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from cart.serializers import BasketSerializer
from products.models import Product


def get_products_in_cart(cart):
    """
    Получение товаров из корзины и их сериализация
    :param cart: корзина товаров
    :return: сериализованные данные
    """
    products_in_cart = [product for product in cart.cart.keys()]
    products = Product.objects.filter(pk__in=products_in_cart)
    serializer = BasketSerializer(products, many=True, context=cart.cart)
    return serializer

class BasketAPIView(APIView):
    """ Класс для создания корзины товаров """
    def get(self, request: Request) -> Response:
        """ Функция для получения корзины и товаров в ней """
        cart = Cart(request)
        serializer = get_products_in_cart(cart)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """ Функция для добавления товаров в козину """
        cart = Cart(request)
        product = get_object_or_404(Product, id=request.data.get('id'))
        cart.add(product=product, quantity=request.data.get('count'))
        serializer = get_products_in_cart(cart)
        return Response(serializer.data)

    def delete(self, request: Request) -> Response:
        """ Функция для удаления товаров из корзины """
        data = json.loads(request.body)
        cart = Cart(request)
        product = get_object_or_404(Product, id=data["id"])
        count = data["count"]
        cart.remove(product, quantity=count)
        serializer = get_products_in_cart(cart)
        return Response(serializer.data)