FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==1.8.2"
#RUN pip install sqlparce

RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY diploma-frontend/dist/diploma-frontend-0.6.tar.gz /app/
RUN pip install diploma-frontend-0.6.tar.gz

COPY marketplace .

#RUN DJANGO_SUPERUSER_PASSWORD=123 python manage.py createsuperuser -h --username admin

#RUN python manage.py makemigrations
#RUN python manage.py migrate

CMD ["gunicorn", "marketplace.wsgi:application", "--bind", "0.0.0.0:8000"]
