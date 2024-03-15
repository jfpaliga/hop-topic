from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Requests(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requester")
    beer_name = models.CharField(max_length=200, unique=True)
    brewery_name = models.CharField(max_length=200, blank=True, null=True)
    image = CloudinaryField('image', default='placeholder')
    abv = models.FloatField()
    first_brewed = models.CharField(max_length=200)
    comments = models.TextField()
    is_approved = models.BooleanField(default=False)
