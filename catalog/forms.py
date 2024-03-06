from django import forms
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import Review


CHOICES = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5,}

class ReviewForm(forms.ModelForm):
    """
    Form class for users to leave a review on a beer 
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            InlineRadios('rating'),
            Field('body')
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