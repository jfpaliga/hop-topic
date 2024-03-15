from django.test import TestCase

from .forms import RequestsForm


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
