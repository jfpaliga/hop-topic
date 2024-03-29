from datetime import datetime
from django.core.cache import cache

from .models import Beer

def get_beer_average_rating(beer):
    """
    Update the beer avg rating when a new review is approved
    """
    ratings = beer.reviews.filter(
        is_approved=True).values_list('rating', flat=True)
    total_ratings = sum(list(ratings))
    return total_ratings / len(ratings) if ratings else 0.0


def get_random_beer_pk():
    """
    Generates a random beer primary key and ensures this pk is the
    same for all users and has also not been used in the last 7
    days by checking the cache for prev_random_beers
    """
    prev_random_beers = cache.get('prev_random_beers')
    if prev_random_beers is None:
        prev_random_beers = []

    today = datetime.now().date()

    if prev_random_beers and prev_random_beers[0]['date'] == today:
        random_beer_pk = prev_random_beers[0]['pk']
    else:
        prev_beer_pks = [ beer['pk'] for beer in prev_random_beers ]
        random_beer = None
        
        while random_beer is None or random_beer.pk in prev_beer_pks:
            random_beer = Beer.objects.order_by('?').first()
        
        random_beer_pk = random_beer.pk
        prev_random_beers.insert(0, {'pk': random_beer_pk,
                                     'date': today})
        prev_random_beers = prev_random_beers[:7]
        cache.set('prev_random_beers', prev_random_beers, timeout=None)

    return random_beer_pk
