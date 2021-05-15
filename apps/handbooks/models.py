from django.contrib.postgres.fields import ArrayField
from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Категория'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Имя'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    def __str__(self):
        return self.name


class Country(models.Model):
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    name = models.CharField(
        max_length=255,
        verbose_name='Название страны'
    )
    cities_id = ArrayField(
        models.PositiveIntegerField(null=True, blank=True),
        null=True,
        blank=True,
        verbose_name='Массив ID стран'
    )

    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    name = models.CharField(
        max_length=255,
        verbose_name='Название города'
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name='Страна'
    )

    def __str__(self):
        return f'{self.name} - {self.country.name}'
