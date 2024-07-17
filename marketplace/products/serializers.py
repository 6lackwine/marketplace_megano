import datetime

from rest_framework import serializers

from products.models import Product, Tag, ProductSpecification, Review, ProductImage, Sale

from django.conf import settings

class TagSerializers(serializers.ModelSerializer):
    """ Класс для сериализации тегов """
    class Meta:
        model = Tag
        fields = ("id", "name",)

class ReviewSerializers(serializers.ModelSerializer):
    """ Класс для сериализации отзывов о товаре """
    date = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = "author", "email", "text", "rate", "date"

    def get_date(self, instance):
        """ Функция возвращает отформатированную дату и время"""
        return datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

class SpecificationsSerializers(serializers.ModelSerializer):
    """ Класс для сериализации характеристик товара """
    class Meta:
        model = ProductSpecification
        fields = "name", "value"

class ProductImageSerializers(serializers.ModelSerializer):
    """ Класс для сериализации изображений товара """
    class Meta:
        model = ProductImage
        fields = "src", "alt"


class ProductSerializers(serializers.ModelSerializer):
    """ Класс для сериализации товаров """
    price = serializers.SerializerMethodField()
    # date = serializers.SerializerMethodField()
    images = ProductImageSerializers(many=True)
    tags = TagSerializers(many=True)
    reviews = ReviewSerializers(many=True)
    specifications = SpecificationsSerializers(many=True)

    def get_price(self, instance):
        """
        Функция для получения стоимости товара
        :param instance: Экземпляр класса
        :return: Стоимость товара
        """
        saleProduct = Sale.objects.filter(product_id=instance.pk)
        salePrice = [i.salePrice for i in saleProduct]
        if salePrice:
            instance.price = salePrice[0]
            instance.save()
        return instance.price

    # def get_date(self, instance):
    #     date = instance.date + datetime.timedelta(hours=3)
    #     return datetime.datetime.strftime(date, '%d.%m.%Y %H:%M')

    class Meta:
        model = Product
        fields = "id", "category", "price", "count", "date", "title", "description", \
            "fullDescription", "freeDelivery", "images", "tags", "reviews", "specifications", "rating"

class ProductsPopularAndLimitedSerializers(serializers.ModelSerializer):
    """ Класс для сериализации популярных и лимитированных товаров"""
    price = serializers.SerializerMethodField()
    images = ProductImageSerializers(many=True)
    tags = TagSerializers(many=True)
    reviews = serializers.IntegerField(source="reviews.count")
    rating = serializers.FloatField()
    class Meta:
        model = Product
        fields = "id", "category", "price", "count", "date", "title", "description", \
            "freeDelivery", "images", "tags", "reviews", "rating"

    def get_price(self, instance):
        """
        Функция для получения стоимости товара
        :param instance: Экземпляр класса
        :return: Стоимость товара
        """
        saleProduct = Sale.objects.filter(product_id=instance.pk)
        salePrice = [i.salePrice for i in saleProduct]
        if salePrice:
            instance.price = salePrice
            #instance.save()
            return salePrice[0]
        return instance.price

class SalesSerializers(serializers.ModelSerializer):
    """ Класс для сериализации скидок на товар"""
    price = serializers.StringRelatedField()
    title = serializers.StringRelatedField()
    images = serializers.SerializerMethodField()
    dateTo = serializers.SerializerMethodField()
    dateFrom = serializers.SerializerMethodField()

    def get_images(self, instance):
        """
        Функция для получения изображения товара
        :param instance: Экземпляр класса
        :return: Изображение товара
        """
        images = []
        images_tmp = instance.product.images.all()
        for image in images_tmp:
            images.append({"src": f"{settings.MEDIA_URL}{image.src}", "alt": image.alt})
        return images

    def get_dateTo(self, instance):
        """
        Функция для получения даты окончания скидки
        :param instance: Экземпляр класса
        :return: Дату в формате день:месяц
        """
        date = instance.dateTo + datetime.timedelta(hours=3)
        return datetime.datetime.strftime(date, '%d.%m')

    def get_dateFrom(self, instance):
        """
        Функция для получения даты начала скидки
        :param instance:
        :return:
        """
        date = instance.dateFrom + datetime.timedelta(hours=3)
        return datetime.datetime.strftime(date, '%d.%m')

    class Meta:
        model = Sale
        fields = "id", "price", "salePrice", "dateFrom", "dateTo", "title", "images",
