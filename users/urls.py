from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewList.as_view(), name='all_reviews'),
    path('<str:username>', views.user_reviews, name="user_reviews")
]
