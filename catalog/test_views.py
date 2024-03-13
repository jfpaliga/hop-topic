from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from .forms import ReviewForm
from .models import Beer

# Create your tests here.
class TestCatalogViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='Username',
            password='Password',
            email='test@test.com'
        )
        self.beer = Beer(
            pk='999',
            name='Beer name',
            tagline='Test beer',
            first_brewed='testdate',
            description='Test description',
            image_url='https://test.com',
            abv=5,
            food_pairing=['testone', 'testtwo', 'testthree'],
            avg_rating=0
        )
        self.beer.save()

    def test_render_beer_detail_page_with_review_form(self):
        """Test for rendering a page with the beer_detail view"""
        response = self.client.get(reverse(
            'beer_detail', args=[999]))
        self.assertEqual(response.status_code, 200, 
                         msg="HTTP request not successful")
        self.assertIn(b"Beer name", response.content, 
                      msg="Name not in view")
        self.assertIn(b"Test beer", response.content, 
                      msg="Tagline not in view")
        self.assertIn(b"Rating: 0", response.content, 
                      msg="Rating not in view")
        self.assertIn(b"https://test.com", response.content, 
                      msg="Image not in view")
        self.assertIn(b"testdate", response.content, 
                      msg="First brewed date not in view")
        self.assertIn(b"5%", response.content, 
                      msg="ABV not in view")
        self.assertIn(b"Test description", response.content, 
                      msg="Description not in view")

        for food in self.beer.food_pairing:
            food_bytes = bytearray(food, 'utf-8')
            self.assertIn(food_bytes, response.content, 
                          msg="Food pairing not in view")

        self.assertIn("reviews_count", response.context, 
                      msg="Reviews count not in view")
        self.assertIn("reviews", response.context, 
                      msg="Reviews not in view")
        self.assertIsInstance(response.context["review_form"], ReviewForm, 
                              msg="review_form is not an instance of ReviewForm")
        
    def test_successful_review_submission(self):
        """Test for leaving a review on a beer"""
        self.client.login(
            username="Username", password="Password"
        )
        review_data = {
            'rating': 5,
            'body': 'This is a test review'
        }
        response = self.client.post(reverse(
            "beer_detail", args=[999]), review_data)
        self.assertEqual(response.status_code, 200, msg="HTTP request not successful")
        self.assertIn(b'User rating: 5', response.content, 
                      msg="Review rating not in review submission")
        self.assertIn(b"This is a test review", response.content, 
                      msg="Review body not in review submission")
