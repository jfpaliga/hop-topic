def get_beer_average_rating(beer):
    """
    Update the beer avg rating when a new review is approved
    """
    ratings = beer.reviews.filter(
        is_approved=True).values_list('rating', flat=True)
    total_ratings = sum(list(ratings))
    return total_ratings / len(ratings) if ratings else 0.0
