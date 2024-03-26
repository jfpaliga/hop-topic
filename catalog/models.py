from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


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


class Requests(models.Model):
    """
    Stores a single request for a beer from a user
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requester")
    beer_name = models.CharField(max_length=200, unique=True)
    brewery_name = models.CharField(max_length=200, blank=True, null=True)
    image = CloudinaryField('image', default='placeholder')
    abv = models.FloatField()
    first_brewed = models.CharField(max_length=200)
    comments = models.TextField()
    is_approved = models.BooleanField(default=False)
