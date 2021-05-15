from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts import SEX
from apps.movie.models import TimestampMixin
from apps.handbooks.models import Country, City


class CustomUser(AbstractUser):
    pass


class Profile(TimestampMixin):
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профиль"

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    first_name = models.CharField(
        max_length=125,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        verbose_name='Город'
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        verbose_name='Страна'
    )
    birthday = models.DateField()
    sex = models.CharField(
        max_length=5,
        choices=SEX,
        verbose_name='Пол'
    )
    avatar = models.ImageField(
        upload_to='avatar',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'
