<h1>Интернет магазин Megano</h1>
<div>
  Это простое веб-приложение для интернет-магазина, разработанное с использованием фреймворка Django. Приложение позволяет пользователям просматривать товары, добавлять их в корзину и оформлять заказы.
</div>
<h2>Особенности</h2>
<ul><li>Просмотр списка товаров</li>
<li>Фильтрация и пагинация каталога</li>
<li>Подробная информация о каждом товаре</li>
<li>Корзина для добавления товаров</li>
<li>Оформление заказа</li>
<li>Личный кабинет</li>
<li>Административная панель для управления товарами и заказами</li>
</ul>
<h2>Установка</h2>
<ul>
  <li>Клонируйте репозиторий:
   ```bash
   git clone https://github.com/6lackwine/marketplace_megano.git
   cd marketplace_megano</li>
  <li>Установите необходимые зависимости: pip install -r requirements.txt</li>
  <li>Подключите frontend: pip install diploma-frontend/dist/diploma-frontend-0.6.tar.gz</li>
  <li>Примените миграции базы данных: python manage.py migrate</li>
  <li>Создайте суперпользователя: python manage.py createsuperuser</li>
  <li>Заполните базу данных тестовыми данными: Для загрузки фикстур в базу данных необходимо ввести команду по каждой фикстуре python manage.py loaddata "имя фикстуры.json"</li>
  <li>Запустите сервер разработки:
python manage.py runserver
Теперь вы можете открыть ваше приложение в браузере по адресу
http://127.0.0.1:8000/</li>
</ul>
Так же можно развернуть приложение с помощью Docker.
<ul>
  <li>Собираем контейнер: docker compose build</li>
  <li>Разворачиваем контейнер: docker compose up</li>
  <li>Теперь вы можете открыть ваше приложение в браузере по адресу
http://127.0.0.1:8030/</li>
</ul>
