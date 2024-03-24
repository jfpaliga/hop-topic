from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Requests, Review


@admin.register(Requests)
class RequestsAdmin(SummernoteModelAdmin):

    list_display = ('user', 'beer_name', 'is_approved')
    search_fields = ['user', 'beer_name']
    list_filter = ('is_approved',)
    summernote_fields = ('comments',)


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):

    list_display = ('author', 'beer', 'rating', 'is_approved',)
    search_fields = ['author', 'rating']
    list_filter = ('is_approved',)
    summernote_fields = ('body',)
