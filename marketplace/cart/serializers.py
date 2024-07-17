from rest_framework import serializers

from products.models import Product, Sale
from products.serializers import TagSerializers, ProductImageSerializers, ProductSerializers


class BasketSerializer(serializers.ModelSerializer):
    """ Класс для сериализации корзины товаров """
    super(ProductSerializers)
    price = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    images = ProductImageSerializers(many=True)
    # tags = TagSerializers(many=True)
    # reviews = serializers.IntegerField(source="reviews.count")
    class Meta:
        model = Product
        fields = "id", "category", "price", "count", "date", "title", "description", \
            "freeDelivery", "images", "tags", "reviews", "rating"

    def get_price(self, instance):
        """
        Функция проверяет если на товаре скидка и применяет ее
        :param instance: Экземпляр класса
        :return: Стоимость со скидкой [int]
        """
        saleProduct = Sale.objects.filter(product_id=instance.pk)
        salePrice = [i.salePrice for i in saleProduct]
        if salePrice:
            instance.price = salePrice[0]
            #instance.save()
            #return salePrice[0]
        return instance.price

    def get_count(self, obj):
        """
        Функция возвращает количество товара добавленного в корзину
        :param obj: Экземпляр класса
        :return: Количество товара в корзине [int]
        """
        return self.context.get(str(obj.pk)).get('quantity')