from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Review
from catalog.utils import get_beer_average_rating

@receiver(post_save, sender=Review)
def save_review(sender, instance, created, **kwargs):
    if instance.is_approved:
        beer = instance.beer
        beer.avg_rating = get_beer_average_rating(beer)
        beer.save()
