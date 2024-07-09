from django import forms
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from datetime import datetime

from catalog.models import Requests, Beer
from users.models import Review

CHOICES = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, }


class RequestsForm(forms.ModelForm):
    """
    Form class for users to request a beer to be added to the database
    """
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Requests
        fields = (
            'beer_name',
            'brewery_name',
            'image',
            'abv',
            'first_brewed',
            'comments',
            )
        widgets = {
            'first_brewed': forms.DateInput(attrs={'type': 'month'}),
        }

    def clean_first_brewed(self):
        """
        Take the cleaned data and reformat into desired string format
        """
        data = self.cleaned_data['first_brewed']
        if isinstance(data, str):
            try:
                data = datetime.strptime(data, '%Y-%m').date()
                data = data.strftime('%m/%Y')
            except ValueError:
                raise forms.ValidationError("Enter a valid date")
        return data


class RequestAdminForm(forms.ModelForm):
    """
    Form class for admins to modify a request
    """
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Requests
        fields = (
            'beer_name',
            'brewery_name',
            'image',
            'abv',
            'first_brewed',
            'comments',
            'is_approved',
            )


class ReviewForm(forms.ModelForm):
    """
    Form class for users to leave a review on a beer
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'reviewForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            InlineRadios('rating'),
            Field('body'),
            Submit('submit', 'Submit', css_id='submitButton'),
        )

    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Review
        fields = ('rating', 'body',)
        widgets = {
            'rating': forms.RadioSelect(choices=CHOICES,)
        }


class BeerForm(forms.ModelForm):
    """
    Form class for adding and editing beers in the
    database in the frontend
    """
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Beer
        fields = (
            'name',
            'tagline',
            'first_brewed',
            'description',
            'beer_image',
            'abv',
            'food_pairing',
            'avg_rating',
        )
