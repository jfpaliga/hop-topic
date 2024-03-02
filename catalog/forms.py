from django import forms
from .models import Review


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