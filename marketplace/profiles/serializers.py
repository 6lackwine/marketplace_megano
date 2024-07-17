from django.contrib.auth.models import User
from rest_framework import serializers

from profiles.models import Profiles, ProfileAvatar


class ProfileAvatarSerializers(serializers.ModelSerializer):
    """ Класс для сериализации изображения профиля """
    class Meta:
        model = ProfileAvatar
        fields = "src", "alt"

class ProfileSerializers(serializers.ModelSerializer):
    """ Класс для сериализации профиля """
    avatar = ProfileAvatarSerializers()
    class Meta:
        model = Profiles
        fields = "fullName", "email", "phone", "avatar"

class UserSerializers(serializers.ModelSerializer):
    """ Класс для сериализации пользователя """
    class Meta:
        model = User
        fields = "username", "password"

class PasswordUpdateSerializers(serializers.ModelSerializer):
    """ Класс для сериалзации пароля """
    class Meta:
        model = User
        fields = "password",