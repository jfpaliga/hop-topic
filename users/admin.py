from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Review


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):

    list_display = ('author', 'beer', 'rating', 'is_approved',)
    search_fields = ['author', 'rating']
    list_filter = ('is_approved',)
    summernote_fields = ('body',)
