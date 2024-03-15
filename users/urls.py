from django.urls import path
from . import views

urlpatterns = [
    path('', views.new_beer_request, name='requests')
]
