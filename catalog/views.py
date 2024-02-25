from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Beer

# Create your views here.
class BeerList(generic.ListView):
    queryset = Beer.objects.all()
    template_name = "catalog/index.html"
    paginate_by = 8

def beer_detail(request, id):
    """
    Display an invidivual :model:`catalog.Beer`.

    **Context**
    ``beer``
        An instance of :model:`catalog.Beer`.

    ** Template**
    :template:`blog/post_detail.html`
    """

    queryset = Beer.objects.all()
    beer = get_object_or_404(queryset, id=id)

    return render(
        request,
        "catalog/beer_detail.html",
        {"beer": beer,},
    )
