def get_beer_average_rating(beer):
    """
    update the beer rating when approved rating is updated
    """
    ratings = beer.reviews.filter(
        is_approved=True).values_list('rating', flat=True)
    total_ratings = sum(list(ratings))
    return total_ratings / len(ratings) if ratings else 0.0
