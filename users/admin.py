from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Requests


@admin.register(Requests)
class RequestsAdmin(SummernoteModelAdmin):

    list_display = ('user', 'beer_name', 'is_approved')
    search_fields = ['user', 'beer_name']
    list_filter = ('is_approved',)
    summernote_fields = ('comments',)
