from django import forms
from datetime import datetime

from .models import Requests


class RequestsForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ('beer_name', 'brewery_name', 'image', 'abv', 'first_brewed', 'comments',)
        widgets = {
            'first_brewed': forms.DateInput(attrs={'type': 'month'}),
        }

    def clean_first_brewed(self):
        data = self.cleaned_data['first_brewed']
        if isinstance(data, str):
            try:
                data = datetime.strptime(data, '%Y-%m').date()
                data = data.strftime('%m/%Y')
            except ValueError:
                raise forms.ValidationError("Enter a valid date")
        return data
