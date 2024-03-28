from django.test import TestCase

from catalog.models import Beer
from .utils import get_random_beer_pk


class TestRandomBeerView(TestCase):
    
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
