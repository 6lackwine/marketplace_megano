from django.urls import path

from cart.views import BasketAPIView

urlpatterns = [
    path("basket", BasketAPIView.as_view(), name="basket"),
]