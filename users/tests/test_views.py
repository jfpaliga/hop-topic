from django.contrib.auth.models import User
from django.urls import reverse
from django.test import RequestFactory, TestCase

from catalog.models import Beer
from users.models import Review
from users.views import ReviewList, user_reviews


class TestAllReviewsPage(TestCase):

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
            beer_image='https://test.com',
            abv=5,
            food_pairing=['testone', 'testtwo', 'testthree'],
            avg_rating=0
        )
        self.beer.save()
        self.review = Review(
            beer=self.beer,
            author=self.user,
            rating=3,
            body='This is a test',
            is_approved=True,
        )
        self.review.save()

    def test_all_reviews_page_view(self):
        """Test all reviews page HTTP request is successful"""
        request = RequestFactory().get('/users/')
        response = ReviewList.as_view()(request)
        self.assertEqual(response.status_code, 200,
                         msg="HTTP request not successful")

    def test_queryset_in_context(self):
        """Test the review_list queryset is in the views context"""
        response = self.client.get(reverse('all_reviews'))
        self.assertIn("review_list", response.context,
                      msg="queryset not in context")

    def test_all_reviews_query_user_exists(self):
        """
        Test if search by username functionality on all_reviews page
        redirects successfully
        """
        # response = self.client.get('/users/?query=Username', follow=True)
        response = self.client.get(reverse('user_reviews',
                                           args=['Username']),
                                   follow=True)
        self.assertEqual(response.status_code, 200,
                         msg="HTTP request not successful")
        self.assertIn(b"Username's Profile", response.content,
                      msg="Username profile not found")

    def test_all_reviews_query_user_does_not_exist(self):
        """
        Test if correct error displays if a query is made for a
        username that does not exist
        """
        response = self.client.get('/users/?query=nonexistentuser',
                                   follow=True)
        self.assertRedirects(response, reverse('all_reviews'))
        self.assertContains(response, "User does not exist!", status_code=200)


class TestUserReviewsPage(TestCase):

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
            beer_image='https://test.com',
            abv=5,
            food_pairing=['testone', 'testtwo', 'testthree'],
            avg_rating=0
        )
        self.beer.save()
        self.review = Review(
            beer=self.beer,
            author=self.user,
            rating=3,
            body='This is a test',
            is_approved=True,
        )
        self.review.save()

    def test_user_reviews_page_view(self):
        """Test user reviews page HTTP request is successful"""
        request = RequestFactory().get('/users/Username')
        response = user_reviews(request, 'Username')
        self.assertEqual(response.status_code, 200,
                         msg="HTTP request not successful")

    def test_user_reviews_context(self):
        """Test all the necessary context is in the view"""
        response = self.client.get(reverse('user_reviews', args=['Username']))
        self.assertIn("user", response.context,
                      msg="User not in context")
        self.assertIn("reviews", response.context,
                      msg="Reviews not in context")
        self.assertIn("reviews_count", response.context,
                      msg="Reviews_count not in context")
