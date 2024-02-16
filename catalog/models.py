from django.db import models

# Create your models here.
class Beer(models.Model):
    """
    Stores information on a single beer
    """
    name = models.CharField(max_length=200, unique=True)
    tagline = models.CharField(max_length=200, unique=True)
    first_brewed = models.DateField()
    description = models.TextField()
    image_url = models.URLField()
    abv = models.IntegerField()
    food_pairing = models.JSONField()
