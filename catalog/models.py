from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Beer(models.Model):
    """
    Stores information on a single beer
    """
    name = models.CharField(max_length=200, unique=True)
    tagline = models.CharField(max_length=200, unique=True)
    first_brewed = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField()
    abv = models.IntegerField()
    food_pairing = models.JSONField()

    def __str__(self):
        return f"{self.name}"
    

class Review(models.Model):
    """
    Stores a single review on a beer related to :model:`auth.User`
    and :model:`catalog.Beer`.
    """
    beer = models.ForeignKey(
        Beer, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewer")
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    body = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Review of {self.beer.name}: {self.rating} by {self.author}"
