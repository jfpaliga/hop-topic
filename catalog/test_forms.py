from django.test import TestCase

from .forms import RequestsForm, ReviewForm


class TestRequestsForm(TestCase):

    def test_form_is_valid(self):
        """Test for all fields"""
        request_form = RequestsForm({
            'beer_name': 'Test',
            'brewery_name': 'Test Brewery',
            'abv': 5.5,
            'first_brewed': '2024-01-01',
            'comments': 'This is a test'
        })
        self.assertTrue(request_form.is_valid(), msg="Form is not valid")


class TestReviewForm(TestCase):

    def test_form_is_valid(self):
        """Test for all fields"""
        review_form = ReviewForm({
            'rating': 5, 
            'body': 'An excellent review'
            })
        self.assertTrue(review_form.is_valid(), msg='Form is not valid')

    def test_rating_is_required(self):
        """Test for the 'rating' field"""
        review_form = ReviewForm({'body': 'This review has no rating'})
        self.assertFalse(review_form.is_valid(), msg='Form is valid')

    def test_body_is_required(self):
        """Test for the 'body' field"""
        review_form = ReviewForm({'rating': 5, 'body': ''})
        self.assertFalse(review_form.is_valid(), msg='Form is valid')
