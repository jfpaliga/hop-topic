from django.db import models
from django.contrib.auth.models import User


class Beer(models.Model):
    """
    Stores information on a single beer
    """
    name = models.CharField(max_length=200, unique=True)
    tagline = models.CharField(max_length=200, unique=True)
    first_brewed = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField()
    abv = models.FloatField()
    food_pairing = models.JSONField()
    avg_rating = models.DecimalField(decimal_places=1, max_digits=2, default=0)

    def __str__(self):
        return f"{self.name}"
