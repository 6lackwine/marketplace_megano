from django.db import models

def category_image_directory_path(instance: "CategoryImage", filename: str) -> str:
    """
    Функция для создания пути до директории с изображениями категорий
    :param instance: Экземпляр класса CategoryImage
    :param filename: Название изображения
    :return: Путь до директории с изображениями [str]
    """
    return "catalog/{category}/icons/{filename}".format(
            category=instance.src,
            filename=filename,
        )
    # if instance.category.subcategories:
    #     return "catalog/{category_parent}/{category}/images/{filename}".format(
    #         category_parent=instance.category.subcategories,
    #         category=instance.category,
    #         filename=filename,
    #     )
    # else:
    #     return "catalog/{category}/icons/{filename}".format(
    #         category=instance.category,
    #         filename=filename,
    #     )

class Categories(models.Model):
    """ Класс для создания модели категории товара """
    title = models.CharField(max_length=100, blank=True, db_index=True, verbose_name="Название")
    image = models.ForeignKey("CategoryImage", on_delete=models.CASCADE, null=True, verbose_name="Изображение")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories", verbose_name="Категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

class CategoryImage(models.Model):
    """ Класс для создания модели изображения категории товара """
    src = models.FileField(upload_to=category_image_directory_path, verbose_name="Путь")
    alt = models.CharField(max_length=100, null=True, verbose_name="Название")
    #category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, related_name="images")

    class Meta:
        verbose_name = "Изображение категории"
        verbose_name_plural = "Изображения категорий"

    def __str__(self):
        return f"{self.alt}"
