from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase

from catalog.models import Beer
from users.models import Review
from .utils import get_random_beer_pk, get_beer_average_rating


class TestGetBeerAvgRating(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='Username',
            password='Password',
            email='test@test.com'
        )
        self.beer = Beer(
            pk='1',
            name='Test',
            tagline='Test beer',
            first_brewed='testdate',
            description='Test description',
            image_url='https://test.com',
            abv=5,
            food_pairing=['testone', 'testtwo', 'testthree'],
            avg_rating=0
        )
        self.beer.save()
        self.review_one = Review(
            beer=self.beer,
            author=self.user,
            rating=3,
            body='This is a test',
            is_approved=True,
        )
        self.review_one.save()
        self.review_two = Review(
            beer=self.beer,
            author=self.user,
            rating=5,
            body='This is a test',
            is_approved=False,
        )
        self.review_two.save()
    
    def test_get_beer_average_rating_one_review(self):
        """Test the average rating function works correctly for one review"""
        avg_rating = get_beer_average_rating(self.beer)
        self.assertEqual(avg_rating, 3, msg="Average rating is not correct")

    def test_get_beer_average_rating_two_reviews(self):
        """Test the average rating function correctly calculates the average"""
        self.review_two.is_approved = True
        self.review_two.save()
        avg_rating = get_beer_average_rating(self.beer)
        self.assertEqual(avg_rating, 4, msg="Average rating is not correct")

    def test_handlers_update_new_reviews(self):
        """
        Test that beer.avg_rating is correct from set up and then test the handler
        correctly updates beer.avg_rating when a new review is approved
        """
        self.assertEqual(self.beer.avg_rating, 3.0,
                         msg="Handler has not updated beer with rating from review_one")
        self.review_two.is_approved = True
        self.review_two.save()
        self.assertEqual(self.beer.avg_rating, 4.0,
                         msg="Handler has not updated beer with rating from review_two")
        
    def test_handlers_delete_review(self):
        """Test the handler correctly updates beer.avg_rating when a review is deleted"""
        self.review_two.is_approved = True
        self.review_two.save()
        self.review_one.delete()
        self.assertEqual(self.beer.avg_rating, 5.0,
                         msg="Handler has not updated beer after review_one is deleted")


class TestGetRandomBeer(TestCase):
    
    def setUp(self):
        self.beer_one = Beer(
            pk='1',
            name='Beer name one',
            tagline='Test beer one',
            first_brewed='testdate',
            description='Test description',
            image_url='https://test.com',
            abv=5,
            food_pairing=['testone', 'testtwo', 'testthree'],
            avg_rating=1
        )
        self.beer_one.save()
        self.beer_two = Beer(
            pk='2',
            name='Beer name two',
            tagline='Test beer two',
            first_brewed='testdate',
            description='Test description',
            image_url='https://test.com',
            abv=11,
            food_pairing=['testone', 'testtwo', 'testthree'],
            avg_rating=2
        )
        self.beer_two.save()
        self.beer_three = Beer(
            pk='3',
            name='Beer name three',
            tagline='Test beer three',
            first_brewed='testdate',
            description='Test description',
            image_url='https://test.com',
            abv=3,
            food_pairing=['testone', 'testtwo', 'testthree'],
            avg_rating=3
        )
        self.beer_three.save()

    def test_random_beer_is_cached(self):
        """
        Test that the random beer pk is cached
        """
        first_instance_of_random_beer = get_random_beer_pk()
        second_instance_of_random_beer = get_random_beer_pk()
        self.assertEqual(first_instance_of_random_beer,
                         second_instance_of_random_beer,
                         msg="Random beer pk is not cached")

    def test_random_beer_is_todays_beer(self):
        """
        Test that the random beer pk is the cached beer pk for today
        """
        today = datetime.now().date()
        cache.set("prev_random_beers", [{'pk': 1, 'date': today}])
        self.assertEqual(get_random_beer_pk(), 1,
                         msg="Random beer pk is not today's beer")
        
    def test_new_random_beer_if_today_not_cached(self):
        """
        Test that if no beer has been cached today, a new beer is cached
        """
        yesterday = date.today() - timedelta(days=1)
        day_before = yesterday - timedelta(days=1)
        cache.set("prev_random_beers", [{'pk': 2, 'date': yesterday},
                                        {'pk': 1, 'date': day_before}])
        self.assertEqual(get_random_beer_pk(), 3,
                         msg="Random beer pk is selecting an already cached beer pk")
        