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
    

class Review(models.Model):
    """
    Stores a single review on a beer related to :model:`auth.User`
    and :model:`catalog.Beer`.
    """
    RATINGS = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        )

    beer = models.ForeignKey(
        Beer, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewer")
    rating = models.IntegerField(default=1, choices=RATINGS)
    body = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Review of {self.beer.name}: {self.rating} by {self.author}"
