from django.urls import path

from orders.views import OrderIDAPIView, OrderAPIView, PaymentAPIView

urlpatterns = [
    path("orders", OrderAPIView.as_view(), name="orders"),
    path("order/<int:pk>", OrderIDAPIView.as_view(), name="order_id"),
    path("payment/<int:pk>", PaymentAPIView.as_view(), name="payment"),
]