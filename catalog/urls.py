from django.urls import path
from . import views

urlpatterns = [
    path("", views.BeerList.as_view(), name="home"),
]
