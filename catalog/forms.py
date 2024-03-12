from django import forms
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

from .models import Review


CHOICES = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5,}

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
            Submit('submit', 'Submit', css_id = 'submitButton'),
        )

    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Review
        fields = ('rating', 'body',)
        widgets ={
            'rating': forms.RadioSelect(choices=CHOICES,)
        }