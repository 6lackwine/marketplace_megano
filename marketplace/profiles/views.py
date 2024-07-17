import json

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, UpdateAPIView, GenericAPIView

from cart.cart import Cart
from marketplace import settings
from profiles.models import Profiles, ProfileAvatar
from profiles.serializers import ProfileSerializers, UserSerializers, PasswordUpdateSerializers

class ProfileAPIView(APIView):
    """ Класс для получения профиля и изменения его данных  """
    permission_classes = [IsAuthenticated]
    def get(self, request: Request) -> Response:
        """ Функция для получения данных профиля. Если профиля нет, то он создается """
        profile = Profiles.objects.get(user=request.user)
        if not profile:
            profile = Profiles.objects.create(user=request.user)
        serialized = ProfileSerializers(profile)
        return Response(serialized.data)
    def post(self, request: Request) -> Response:
        """ Функция для изменения данных профиля """
        profile = Profiles.objects.get_or_create(user_id=request.user.pk)
        profile[0].fullName = request.data["fullName"]
        profile[0].phone = request.data["phone"]
        profile[0].email = request.data["email"]
        profile[0].save()
        return Response(request.data, status=200)

class ProfileAvatarAPIView(APIView):
    """ Класс для получения изображения профиля """
    def post(self, request: Request) -> Response:
        """ Функция для добавления или изменения изображения профиля """
        profile = Profiles.objects.get(user_id=request.user.pk)
        avatar = ProfileAvatar.objects.get_or_create(profile_id=profile.pk)
        avatar[0].src = request.FILES["avatar"]
        avatar[0].src.save(name=request.FILES["avatar"], content=request.FILES["avatar"])
        return Response(status=200)

class ProfilePasswordAPIView(UpdateAPIView):
    """ Класс для изменения пароля """
    def post(self, request: Request) -> Response:
        """ Функция изменяет пароль """
        currentUser = User.objects.get(pk=request.user.pk)
        currentPassword = request.data.get("currentPassword")
        if currentPassword != currentUser.password:
            return Response(status=400)
        currentUser.password = request.data.get("newPassword")
        return Response(status=200)


# class ProfileAPIView(RetrieveUpdateAPIView):
#     queryset = Profiles.objects.all()
#     serializer_class = ProfileSerializers
#
#     def get_object(self):
#         queryset = self.filter_queryset(self.get_queryset())
#         obj = queryset.get(pk=self.request.user.pk)
#         self.check_object_permissions(self.request, obj)
#         return obj

class SignUpAPIView(APIView):
    """ Класс для регистрации пользователя """
    def post(self, request: Request) -> Response:
        """ Функция регистрирует пользователя, аутентифицирует и авторизирует его """
        user_data = json.loads(request.body)
        name = user_data["name"]
        username = user_data["username"]
        password = user_data["password"]
        User.objects.create_user(
            username=username,
            first_name=name,
            password=password
        )
        user = authenticate(request, username=username, password=password)
        Profiles.objects.create(user=user)
        if user is not None:
            login(request, user)
            return Response(status=200)
        else:
            return Response()

@api_view(["POST"])
def sign_out(request: Request):
    """ Функция для деавторизации пользователя """
    logout(request)
    return reverse_lazy('profiles:login')

@api_view(["POST"])
def sign_in(request: Request) -> Response:
    """ Функция для аутентификации и авторизации пользователя """
    if request.method == "POST":
        user_data = json.loads(request.body)
        username = user_data["username"]
        password = user_data["password"]
        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user is not None:
            login(request, user)
            return Response(status=200)
        else:
            return Response(status=401)
    # return Response("good", status=200)

    # if request.method == "POST":
    #     json_string = request.body.decode('utf-8')
    #     data_dict = json.loads(json_string)
    #     username = data_dict['username']
    #     password = data_dict['password']
    #     if username and password:
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return HttpResponse(status=200)
