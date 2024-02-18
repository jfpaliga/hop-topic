from django.shortcuts import render
from django.views import generic
from .models import Beer

# Create your views here.
class BeerList(generic.ListView):
    queryset = Beer.objects.all()
    template_name = "beer_list.html"
