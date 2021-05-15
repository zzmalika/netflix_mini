from django.db import models
from datetime import date

from apps.common.models import TimestampMixin
from apps.handbooks.models import Category, Genre


class Actor(models.Model):
    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"

    name = models.CharField(
        max_length=512,
        verbose_name='Ф.И.О'
    )
    age = models.PositiveSmallIntegerField(
        verbose_name='Возраст'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to="actors/",
        verbose_name='Изображение'
    )

    def __str__(self):
        return self.name


class Movie(TimestampMixin):
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    title = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    tagline = models.CharField(
        max_length=100,
        verbose_name='Слоган'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    poster = models.ImageField(
        upload_to="movies/",
        verbose_name='Постер'
    )
    year = models.PositiveSmallIntegerField(
        default=2021,
        verbose_name="Дата выхода"
    )
    country = models.CharField(
        max_length=30,
        verbose_name="Страна"
    )
    directors = models.ManyToManyField(
        Actor,
        verbose_name="Режиссеры",
        related_name="film_director"
    )
    actors = models.ManyToManyField(
        Actor,
        verbose_name="Актеры",
        related_name="film_actor"
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name="Жанры"
    )
    world_premiere = models.DateField(
        default=date.today,
        verbose_name="Премьера в мире",
    )
    budget = models.PositiveIntegerField(
        "Бюджет",
        default=0,
        help_text="указывать сумму в долларах"
    )
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США",
        default=0,
        help_text="указывать сумму в долларах"
    )
    fess_in_world = models.PositiveIntegerField(
        "Сборы в мире",
        default=0,
        help_text="указывать сумму в долларах"
    )
    net_income = models.PositiveIntegerField(
        "Чистая прибыль",
        blank=True,
        help_text="указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
    )
    draft = models.BooleanField(
        default=False,
        verbose_name="Черновик"
    )

    def save(self, *args, **kwargs):
        self.net_income = self.fess_in_world - self.budget
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_review(self):
        return self.reviews.filter(parent__isnull=True)


class MovieShots(TimestampMixin):
    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"

    title = models.CharField(
        max_length=100,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to="movie_shots/",
        verbose_name="Изображение"
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="Фильм"
    )

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["value"]

    value = models.SmallIntegerField("Значение", default=1)

    def save(self, *args, **kwargs):
        if self.value < 0:
            self.value = 0
        elif self.value > 5:
            self.value = 5
        self.value = int(self.value)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.value}'


class Rating(TimestampMixin):
    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    ip = models.CharField(
        max_length=15,
        verbose_name="IP адрес"
    )
    star = models.ForeignKey(
        RatingStar,
        on_delete=models.CASCADE,
        verbose_name="Звезда"
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name="фильм"
    )

    def __str__(self):
        return f"{self.star} - {self.movie}"


class Review(TimestampMixin):
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    email = models.EmailField()
    name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    text = models.TextField(
        max_length=5000,
        verbose_name="Сообщение"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
        verbose_name="Родитель"
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="фильм"
    )

    def __str__(self):
        return f"{self.name} - {self.movie}"
