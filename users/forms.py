from django import forms
from datetime import datetime

from .models import Requests


class MonthYearWidget(forms.widgets.DateInput):
    input_type = 'month'

    def format_value(self, value):
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m').date()
        if value is not None:
            print(value, type(value))
            return value


class RequestsForm(forms.ModelForm):
    first_brewed = forms.DateField(widget=MonthYearWidget)

    class Meta:
        model = Requests
        fields = ('beer_name', 'brewery_name', 'image', 'abv', 'first_brewed', 'comments',)
