from django import forms
from .models import Review


CHOICES = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5,}

class ReviewForm(forms.ModelForm):
    """
    Form class for users to leave a review on a beer 
    """
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Review
        fields = ('rating', 'body',)
        widgets ={
            'rating': forms.RadioSelect(choices=CHOICES),
        }