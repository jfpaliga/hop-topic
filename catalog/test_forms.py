from django.test import TestCase

from .forms import ReviewForm


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
