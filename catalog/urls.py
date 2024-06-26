from django.urls import path

from . import views

urlpatterns = [
    path('', views.BeerList.as_view(), name='home'),
    path('<int:id>/', views.beer_detail, name='beer_detail'),
    path('<int:id>/delete_review/<int:review_id>',
         views.delete_review, name='delete_review'),
    path('<int:id>/edit_review/<int:review_id>',
         views.edit_review, name='edit_review'),
    path('beeroftheday', views.beer_of_the_day, name='beer_of_the_day'),
    path('filter/<filter_type>/<filter_set>',
         views.BeerFilterList.as_view(), name='filter'),
    path('requests', views.new_beer_request, name='requests')
]
