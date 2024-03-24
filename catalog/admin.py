from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Beer, Requests


@admin.register(Beer)
class BeerAdmin(SummernoteModelAdmin):

    list_display = ('name', 'tagline', 'abv',)
    search_fields = ['name', 'abv']
    summernote_fields = ('description',)


@admin.register(Requests)
class RequestsAdmin(SummernoteModelAdmin):

    list_display = ('user', 'beer_name', 'is_approved')
    search_fields = ['user', 'beer_name']
    list_filter = ('is_approved',)
    summernote_fields = ('comments',)
