from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Beer


@admin.register(Beer)
class BeerAdmin(SummernoteModelAdmin):

    list_display = ('name', 'tagline', 'abv',)
    search_fields = ['name', 'abv']
    summernote_fields = ('description',)
