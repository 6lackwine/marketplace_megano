from django.contrib.auth.models import User
from django.db import models


class Profiles(models.Model):
    """ Класс для создания модели профиля """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="users", verbose_name="Пользователь")
    fullName = models.CharField(max_length=100, verbose_name="Фамилия Имя Отчество")
    email = models.EmailField(max_length=50, unique=True, null=True)
    phone = models.CharField(max_length=12, unique=True, verbose_name="Телефон", null=True)
    image = models.ForeignKey("ProfileAvatar", on_delete=models.CASCADE, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return str(self.user)

def profile_avatar_path(instance: "ProfileAvatar", alt: str) -> str:
    """
    Функция создает путь до изображения профиля
    :param instance:
    :param alt: Название изображения [str]
    :return: Путь до изображения [str]
    """
    return "profile/profile_{pk}/users/{alt}".format(
        pk=instance.profile.pk,
        alt=alt,
    )

class ProfileAvatar(models.Model):
    """ Класс для создания модели изображения профиля """
    profile = models.OneToOneField(Profiles, on_delete=models.CASCADE, related_name="avatar", verbose_name="Профиль")
    src = models.FileField(upload_to=profile_avatar_path, verbose_name="Путь")
    alt = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Изображение профиля"