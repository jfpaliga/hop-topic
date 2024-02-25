from django.urls import path
from . import views

urlpatterns = [
    path("", views.BeerList.as_view(), name="home"),
    path('<int:id>/', views.beer_detail, name="beer_detail"),
]
