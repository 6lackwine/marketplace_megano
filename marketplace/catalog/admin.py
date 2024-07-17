from django.contrib import admin

from catalog.models import Categories, CategoryImage

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    """ Класс для управления категориями в админке """
    list_display = "pk", "title", "parent"
    fieldsets = [
        (None, {
            "fields": ("title", "parent", "image")
        }),
    ]
    search_fields = ["title", "parent__title"]

@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    """ Класс для управления изображениями категорий в админке """
    list_display = "pk", "src", "alt"
    fieldsets = [
        (None, {
            "fields": ("src", "alt")
        })
    ]
    search_fields = ["alt", "src"]