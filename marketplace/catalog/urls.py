from django.urls import path

from catalog.views import CategoryAPIView, CatalogAPIView

urlpatterns = [
    path("categories/", CategoryAPIView.as_view(), name="categories"),
    path("catalog/", CatalogAPIView.as_view(), name="catalog_list"),
]