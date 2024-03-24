from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q

from catalog.models import Beer
from users.models import Review
from .forms import RequestsForm, ReviewForm
from .utils import get_random_beer_pk


class BeerList(generic.ListView):
    template_name = "catalog/index.html"
    paginate_by = 8

    def get_queryset(self):
        queryset = Beer.objects.all().order_by("-avg_rating")

        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(tagline__icontains=query) | 
                Q(description__icontains=query)
            ).values()

        return queryset
    

class BeerFilterList(BeerList):
    
    def get_queryset(self):
        if self.kwargs['filter_type'] == 'rating':
            queryset = Beer.objects.filter(avg_rating=int(self.kwargs['filter_set']))
        elif self.kwargs['filter_type'] == 'abv':
            if self.kwargs['filter_set'] == 'lt5':
                queryset = Beer.objects.filter(abv__lt=5)
            elif self.kwargs['filter_set'] == '5to10':
                queryset = Beer.objects.filter(abv__gte=5, abv__lte=10)
            elif self.kwargs['filter_set'] == 'gt10':
                queryset = Beer.objects.filter(abv__gt=10)

        return queryset
   

def beer_detail(request, id):
    """
    Display an invidivual :model:`catalog.Beer`.

    **Context**
    ``beer``
        An instance of :model:`catalog.Beer`.

    ** Template**
    :template:`catalog/beer_detail.html`
    """

    queryset = Beer.objects.all()
    beer = get_object_or_404(queryset, id=id)
    reviews = beer.reviews.all().order_by("-created_on")
    reviews_count = beer.reviews.filter(is_approved=True).count()

    if request.method == "POST":
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.author = request.user
            review.beer = beer
            review.save()
            messages.add_message(
                request, messages.SUCCESS,
                "Your review has been submitted and is awaiting approval"
            )

    review_form = ReviewForm()

    context = {
        "beer": beer,
        "reviews": reviews,
        "reviews_count": reviews_count,
        "review_form": review_form,
        }

    return render(
        request,
        "catalog/beer_detail.html",
        context,
    )


def beer_of_the_day(request):
    """
    View to display a random beer. The random beer is the
    same for each user and will not be the same as another
    random beer from the past 7 days.
    """
    random_beer = get_random_beer_pk()
    return redirect('beer_detail', id=random_beer)


def edit_review(request, id, review_id):
    """
    View to edit reviews
    """
    if request.method == "POST":

        queryset = Beer.objects.all()
        beer = get_object_or_404(queryset, id=id)
        review = get_object_or_404(Review, pk=review_id)
        review_form = ReviewForm(data=request.POST, instance=review)

        if review_form.is_valid() and review.author == request.user:
            review = review_form.save(commit=False)
            review.beer = beer
            review.is_approved = False
            review.save()
            messages.add_message(request, messages.SUCCESS, 'Review Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating review!')

    return HttpResponseRedirect(reverse('beer_detail', args=[id]))


def delete_review(request, id, review_id):
    """
    View to delete reviews
    """
    queryset = Beer.objects.all()
    beer = get_object_or_404(queryset, id=id)
    review = get_object_or_404(Review, pk=review_id)

    if review.author == request.user:
        review.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own reviews!')

    return HttpResponseRedirect(reverse('beer_detail', args=[id]))


def new_beer_request(request):
    request_form = RequestsForm()

    if request.method == "POST":
        request_form = RequestsForm(data=request.POST)
        if request_form.is_valid():
            beer_request = request_form.save(commit=False)
            beer_request.user = request.user
            beer_request.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Request receieved - we will look into adding your beer to the database shortly'
            )

    return render(
        request,
        "catalog/new_beer_request.html",
        {
            "request_form": request_form
        }
    )
