from decimal import Decimal

from marketplace import settings

from products.models import Product

class Cart(object):
    """ Класс корзины """
    def __init__(self, request):
        """ Инициализация корзины """
        self.session = request.session # Запоминаем текущую сессию
        cart = self.session.get(settings.CART_SESSION_ID) # Получаем данные корзины
        if not cart:
            # Сохраняем пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart # Возвращаем корзину

    def __iter__(self):
        """ Перебираем товары в корзине и получаем их из базы данных """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids) # Получаем товары и добавляем в корзину

        cart = self.cart.copy() # Создаем копию корзины
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["totalPrice"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """ Считаем сколько товаров в корзине """
        return sum(item["quantity"] for item in self.cart.values())


    def add(self, product: Product, quantity=1, update_quantity=False):
        # quantity - количество товаров (по умолчанию = 1)
        # update_quantity - значение, которое говорит нужно ли изменить значение количества товара
        # на новое или добавить к существующему (False - добавить к существующему)
        """ Добавляем товар в корзину или обновляем его количество """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if update_quantity: # Обновление корзины
            self.cart[product_id]["quantity"] = quantity # Добавляем товар в корзину
        else:
            self.cart[product_id]["quantity"] += quantity # Если товар имеется, то добавляем количество
        self.save()

    def save(self):
        """ Сохраняем товары в корзине """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product, quantity):
        """ Удаляем товар из корзины """
        product_id = str(product.id)
        if product_id in self.cart:
            if quantity == 1 and self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= int(quantity)
            else:
                del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """ Получаем общую стоимость """
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        """ Очищаем корзину в сессии """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True