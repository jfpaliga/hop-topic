from django.contrib.auth.models import User
from django.urls import reverse
from django.test import RequestFactory, TestCase

from catalog.forms import ReviewForm, RequestsForm
from catalog.models import Beer
from users.models import Review
from catalog.views import BeerList, BeerFilterList
from catalog.utils import get_random_beer_pk


class TestHomePage(TestCase):

    def setUp(self):
        self.beer = Beer(
            pk='1',
            name='Buzz',
            tagline='A Real Bitter Experience',
            first_brewed='09/2007',
            description='Test description',
            image_url='https://test.com',
            abv=5,
            food_pairing=['testone', 'testtwo', 'testthree'],
            avg_rating=0
        )
        self.beer.save()

    def test_home_page_view(self):
        """Test home page HTTP request is successful"""
        request = RequestFactory().get('/')
        response = BeerList.as_view()(request)
        self.assertEqual(response.status_code, 200,
                         msg="HTTP request not successful")

    def test_home_page_query_by_name(self):
        """Test search by name functionality on home page"""
        request = RequestFactory().get('/?query=buzz')
        request.session = {}
        response = BeerList.as_view()(request)
        response.render()
        self.assertIn(b"A Real Bitter Experience", response.content,
                      msg="Query by name unsuccessful")

    def test_home_page_query_by_tagline(self):
        """Test search by tagline functionality on home page"""
        request = RequestFactory().get('/?query=bitter')
        request.session = {}
        response = BeerList.as_view()(request)
        response.render()
        self.assertIn(b"A Real Bitter Experience", response.content,
                      msg="Query by tagline unsuccessful")

    def test_home_page_query_by_description(self):
        """Test search by description functionality on home page"""
        request = RequestFactory().get('/?query=description')
        request.session = {}
        response = BeerList.as_view()(request)
        response.render()
        self.assertIn(b"A Real Bitter Experience", response.content,
                      msg="Query by description unsuccessful")


class TestBeerFilterView(TestCase):

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
            avg_rating=4
        )
        self.beer_three.save()

    def test_filter_page_view(self):
        """Test filtered home page HTTP request is successful"""
        request = RequestFactory().get('/filter/rating/1')
        response = BeerFilterList.as_view()(request,
                                            filter_type='rating',
                                            filter_set='1')
        self.assertEqual(response.status_code, 200,
                         msg="HTTP request not successful")

    def test_filter_by_rating_view(self):
        """Test filter by rating functionality"""
        request = RequestFactory().get('/filter/rating/1')
        request.session = {}
        response = BeerFilterList.as_view()(request,
                                            filter_type='rating',
                                            filter_set='1')
        response.render()
        self.assertIn(b"Beer name one", response.content,
                      msg="Unfiltered queries are not visible")
        self.assertNotIn(b"Beer name two", response.content,
                         msg="Filtered queries are visible")
        self.assertNotIn(b"Beer name three", response.content,
                         msg="Filtered queries are visible")

    def test_filter_by_abv_lt5_view(self):
        """Test filter by abv lt5 functionality"""
        request = RequestFactory().get('/filter/abv/lt5')
        request.session = {}
        response = BeerFilterList.as_view()(request,
                                            filter_type='abv',
                                            filter_set='lt5')
        response.render()
        self.assertIn(b"Beer name three", response.content,
                      msg="Unfiltered queries are not visible")
        self.assertNotIn(b"Beer name one", response.content,
                         msg="Filtered queries are visible")
        self.assertNotIn(b"Beer name two", response.content,
                         msg="Filtered queries are visible")

    def test_filter_by_abv_5to10_view(self):
        """Test filter by abv 5to10 functionality"""
        request = RequestFactory().get('/filter/abv/5to10')
        request.session = {}
        response = BeerFilterList.as_view()(request,
                                            filter_type='abv',
                                            filter_set='5to10')
        response.render()
        self.assertIn(b"Beer name one", response.content,
                      msg="Unfiltered queries are not visible")
        self.assertNotIn(b"Beer name two", response.content,
                         msg="Filtered queries are visible")

    def test_filter_by_abv_gt10_view(self):
        """Test filter by abv gt10 functionality"""
        request = RequestFactory().get('/filter/abv/gt10')
        request.session = {}
        response = BeerFilterList.as_view()(request,
                                            filter_type='abv',
                                            filter_set='gt10')
        response.render()
        self.assertIn(b"Beer name two", response.content,
                      msg="Unfiltered queries are not visible")
        self.assertNotIn(b"Beer name one", response.content,
                         msg="Filtered queries are visible")
        self.assertNotIn(b"Beer name one", response.content,
                         msg="Filtered queries are visible")


class TestBeerDetailView(TestCase):

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
        self.review = Review(
            pk='1',
            beer=self.beer,
            author=self.user,
            rating=3,
            body='This is a test',
            is_approved=True
            )
        self.review.save()

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
        self.assertIn(b"Rating: 3", response.content,
                      msg="Rating not in view")
        self.assertIn(b"https://test.com", response.content,
                      msg="Image not in view")
        self.assertIn(b"testdate", response.content,
                      msg="First brewed date not in view")
        self.assertIn(b"5.0%", response.content,
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
                              msg="review_form not an instance of ReviewForm")

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
        self.assertEqual(response.status_code, 200,
                         msg="HTTP request not successful")
        self.assertIn(b'Rating: 5', response.content,
                      msg="Review rating not in review submission")
        self.assertIn(b"This is a test review", response.content,
                      msg="Review body not in review submission")

    def test_successful_review_edit(self):
        """Test for editing a review"""
        self.client.login(
            username="Username", password="Password"
        )
        review_edit = {
            'rating': 5,
            'body': 'Test edit'
        }
        response = self.client.post(reverse(
            'edit_review', kwargs={'id': 999, 'review_id': 1}),
            review_edit, follow=True)
        self.assertEqual(response.status_code, 200,
                         msg="HTTP request not successful")
        self.assertIn(b'Rating: 5', response.content,
                      msg="Rating not updated")
        self.assertIn(b'Test edit', response.content,
                      msg='Body not updated')

    def test_successful_review_delete(self):
        """Test for deleting a review"""
        self.client.login(
            username="Username", password="Password"
        )
        response = self.client.post(reverse(
            'delete_review', kwargs={'id': 999, 'review_id': 1}),
            follow=True)
        self.assertEqual(response.status_code, 200,
                         msg="HTTP request not successful")
        self.assertNotIn(b'This is a test', response.content,
                         msg='Review not deleted')


class TestBeerOfTheDayView(TestCase):

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

    def test_beer_of_the_day_view(self):
        """Test beer of the day view is successful"""
        beer = get_random_beer_pk()
        response = self.client.get(reverse('beer_detail',
                                           args=[beer]))
        self.assertEqual(response.status_code, 200,
                         msg="HTTP request not successful")
        self.assertIn(b'Beer name one', response.content,
                      msg='Beer detail not displayed')


class TestNewBeerRequestView(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='Username',
            password='Password',
            email='test@test.com'
        )

    def test_render_request_page_with_form(self):
        """Test for rendering a page with the requests view"""
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200,
                         msg="HTTP request not successful")
        self.assertIsInstance(response.context["request_form"], RequestsForm,
                              msg="form not an instance of RequestsForm")

    def test_successful_request_submission(self):
        """Test for leaving a request for a beer"""
        self.client.login(
            username="Username", password="Password"
        )
        request_data = {
            'beer_name': 'Test',
            'brewery_name': 'Test brewery',
            'abv': 5.5,
            'first_brewed': '2024-01',
            'comments': 'This is a test'
        }
        response = self.client.post(reverse(
            "requests"), request_data)
        self.assertEqual(response.status_code, 200,
                         msg="HTTP request not successful")
        self.assertIn(b"Request received", response.content,
                      msg="Request not submitted successfully")
