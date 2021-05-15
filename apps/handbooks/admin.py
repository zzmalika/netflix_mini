from django.contrib import admin

from apps.handbooks.models import Category, Genre, City, Country


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Страны"""
    list_display = ("name",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Города"""
    list_display = ("name",)
