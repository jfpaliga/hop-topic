"""
URL configuration for hoptopic project.

"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('users/', include('users.urls'), name='users-urls'),
    path('', include('catalog.urls'), name='catalog-urls'),
]
