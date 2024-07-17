from django.urls import path

from products.views import TagsList, ProductDetail, ReviewCreate, ProductsPopular, ProductsLimited, SalesAPIView, \
    BannersAPIView

urlpatterns = [
    path("product/<int:pk>/", ProductDetail.as_view(), name="product_detail"),
    path("product/<int:pk>/reviews", ReviewCreate.as_view(), name="create_review"),
    path("products/popular/", ProductsPopular.as_view(), name="products_popular"),
    path("products/limited/", ProductsLimited.as_view(), name="products_limited"),
    path("tags/", TagsList.as_view(), name="tags_list"),
    path("sales/", SalesAPIView.as_view(), name="sales_products"),
    path("banners/", BannersAPIView.as_view(), name="banners_list"),

]