from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.views import APIView

from cart.cart import Cart
from orders.models import Order, ProductOrderCount
from orders.serializers import OrderSerializer
from products.models import Product
from profiles.models import Profiles


class OrderAPIView(APIView):
    """ Класс для получения активных заказов """
    def get(self, request: Request) -> Response:
        """ Функция дял получения заказов """
        order = Order.objects.filter(user_id=request.user.users.pk).order_by("-createdAt")
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """ Функция для создания заказов """
        profile = Profiles.objects.get(user=request.user.pk)
        products_in_order = [
            (
                product["id"],
                product["count"],
                product["price"]
            )
            for product in request.data
        ]
        products = Product.objects.filter(id__in=[product[0] for product in products_in_order])
        order = Order.objects.create(
            user=profile,
            totalCost=Cart(request).get_total_price(),
        )
        data = {
            "orderId": order.pk,
        }
        order.products.set(products)
        order.save()
        return Response(data)

class OrderIDAPIView(APIView):
    """ Класс для получения заказов и их оформления """
    def get(self, request: Request, pk: int) -> Response:
        """ Функция для получения товаров собранных пользователем в корзину """
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        cart = Cart(request).cart
        try:
            products_in_order = order.products
            query = ProductOrderCount.objects.filter(order_id=order.pk)
            count_products = {product.products.pk: product.count for product in query}
            for count_product in products_in_order.all():
                count_product.count = count_products[count_product.pk]
        except:
            products_in_order = order.products
            for count_product in products_in_order.all():
                count_product.count = cart[str(count_product.pk)]["quantity"]
                count_product.save()
        return Response(serializer.data)

    def post(self, request: Request, pk: int) -> Response:
        """ Функция для подтверждения заказов """
        order = Order.objects.get(pk=pk)
        order.fullName = request.data["fullName"]
        order.phone = request.data["phone"]
        order.email = request.data["email"]
        order.city = request.data["city"]
        order.address = request.data["address"]
        order.paymentType = request.data["paymentType"]
        order.status = "Ожидает оплаты"
        order.deliveryType = request.data["deliveryType"]
        if order.deliveryType == "express":
            order.totalCost += 500
        else:
            if order.totalCost < 2000:
                # if request.data["totalCost"] < 2000:
               order.totalCost += 200

        for product in request.data["products"]:
            ProductOrderCount.objects.get_or_create(
                order_id=order.pk,
                products_id=product["id"],
                count=product["count"],
            )

        data = {
            "orderId": order.pk,
        }
        order.save()
        Cart(request).clear()
        return Response(data, status=200)

class PaymentAPIView(APIView):
    """ Класс для фиктивной оплаты заказов """
    def post(self, request: Request, pk: int) -> Response:
        """ Функция проверяет 'Достаточно ли средств' на балансе и производит оплату  """
        order = Order.objects.get(pk=pk)
        number = request.data["number"]
        print(request.data)
        print(order.paymentType)
        # if order.paymentType == "online":
        #print(int(number.split()[3][3]))
        print(number.split())
        if len(number) == 8 and int(number) % 2 == 0 and (int(number) % 10) != 0:
            order.status = "Оплачено"
        else:
            order.status = "Ошибка оплаты, недостаточно средств"
        # elif order.paymentType == "someone":
        #     print(request.data)
        #     if len(number) == 7 and int(number.split()[3]) % 2 == 0 and int(number.split()[3][3]) != 0:
        #         order.status = "Оплачено"
        #     else:
        #         order.status = "Ошибка оплаты, недостаточно средств"
        order.save()
        return Response(status=200)