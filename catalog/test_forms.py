from django.test import TestCase

from catalog.forms import RequestsForm, ReviewForm


class TestRequestsForm(TestCase):

    def test_form_is_valid(self):
        """Test for all fields"""
        request_form = RequestsForm({
            'beer_name': 'Test123',
            'brewery_name': 'Test Brewery',
            'abv': 5.5,
            'first_brewed': '2024-01',
            'comments': 'This is a test'
        })
        print(request_form.errors)
        self.assertTrue(request_form.is_valid(), msg="Form is not valid")

    def test_beer_name_is_not_valid(self):
        """Test for beer name field"""
        request_form = RequestsForm({
            'beer_name': '',
            'brewery_name': 'Test Brewery',
            'image': 'https://placehold.co/600x400/EEE/31343C',
            'abv': 5.5,
            'first_brewed': '2024-01',
            'comments': 'This is a test'
        })
        self.assertFalse(request_form.is_valid(), msg="Beer name is valid")

    def test_abv_is_not_empty(self):
        """Test that abv field is not empty"""
        request_form = RequestsForm({
            'beer_name': 'Test123',
            'brewery_name': 'Test Brewery',
            'image': 'https://placehold.co/600x400/EEE/31343C',
            'abv': '',
            'first_brewed': '2024-01',
            'comments': 'This is a test'
        })
        self.assertFalse(request_form.is_valid(), msg="Abv is valid")

    def test_abv_is_not_string(self):
        """Test that abv field is not a string"""
        request_form = RequestsForm({
            'beer_name': 'Test123',
            'brewery_name': 'Test Brewery',
            'image': 'https://placehold.co/600x400/EEE/31343C',
            'abv': '5.5',
            'first_brewed': '2024-01',
            'comments': 'This is a test'
        })
        self.assertFalse(type(request_form['abv']) == float, msg="Abv is a float")

    def test_first_brewed_is_not_empty(self):
        """Test for first_brewed field"""
        request_form = RequestsForm({
            'beer_name': 'Test123',
            'brewery_name': 'Test Brewery',
            'image': 'https://placehold.co/600x400/EEE/31343C',
            'abv': 5.5,
            'first_brewed': '',
            'comments': 'This is a test'
        })
        self.assertFalse(request_form.is_valid(), msg="First brewed is valid")

    def test_first_brewed_is_not_valid(self):
        """Test for first_brewed field"""
        request_form = RequestsForm({
            'beer_name': 'Test123',
            'brewery_name': 'Test Brewery',
            'image': 'https://placehold.co/600x400/EEE/31343C',
            'abv': 5.5,
            'first_brewed': '01/2024',
            'comments': 'This is a test'
        })
        self.assertFalse(request_form.is_valid(), msg="First brewed is valid")

    def test_comments_is_not_valid(self):
        """Test for comments field"""
        request_form = RequestsForm({
            'beer_name': 'Test123',
            'brewery_name': 'Test Brewery',
            'image': 'https://placehold.co/600x400/EEE/31343C',
            'abv': 5.5,
            'first_brewed': '2024-01',
            'comments': ''
        })
        self.assertFalse(request_form.is_valid(), msg="Comments is valid")

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
