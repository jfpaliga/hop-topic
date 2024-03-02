from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Beer, Review


@admin.register(Beer)
class BeerAdmin(SummernoteModelAdmin):

    list_display = ('name', 'tagline', 'first_brewed',)
    search_fields = ['name', 'abv']
    summernote_fields = ('description',)


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):

    list_display = ('author', 'rating', 'is_approved',)
    search_fields = ['author', 'rating']
    list_filter = ('is_approved',)
    summernote_fields = ('body',)