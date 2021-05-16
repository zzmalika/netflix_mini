from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.handbooks.models import Country, City


@receiver(post_delete, sender=City)
def remove_city_id_from_country(sender, **kwargs):
    pass


@receiver(post_save, sender=City)
def add_city_id_from_country(instance, *args, **kwargs):
    print('asd')
    country = Country.objects.filter(id=instance.country_id).first()
    if country:
        country.cities_id.append(instance.id)
        country.save()
