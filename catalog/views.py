from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse_lazy

from catalog.models import Beer, Requests
from users.models import Review
from .forms import RequestsForm, RequestAdminForm, ReviewForm, BeerForm
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
            queryset = Beer.objects.filter(
                avg_rating=int(self.kwargs['filter_set'])
                ).order_by("-avg_rating")
        elif self.kwargs['filter_type'] == 'abv':
            if self.kwargs['filter_set'] == 'lt5':
                queryset = Beer.objects.filter(
                    abv__lt=5).order_by("-avg_rating")
            elif self.kwargs['filter_set'] == '5to10':
                queryset = Beer.objects.filter(
                    abv__gte=5,
                    abv__lte=10).order_by("-avg_rating")
            elif self.kwargs['filter_set'] == 'gt10':
                queryset = Beer.objects.filter(
                    abv__gt=10).order_by("-avg_rating")

        return queryset
    

class ManageBeersList(LoginRequiredMixin, generic.ListView):
    """
    Shows page to to create, read, update or delete beers
    in the database from the frontend
    """
    model = Beer
    queryset = Beer.objects.order_by("-id")
    template_name = "catalog/manage_beers.html"
    paginate_by = 8


class ManageRequestsList(LoginRequiredMixin, generic.ListView):
    """
    Shows page to create, read, update or delete requests
    in the database from the frontend
    """
    model = Requests
    queryset = Requests.objects.order_by("-id")
    template_name = "catalog/manage_requests.html"
    paginate_by = 8


class ManageReviewsList(LoginRequiredMixin, generic.ListView):
    """
    Shows page to create, read, update or delete requests
    in the database from the frontend
    """
    model = Review
    queryset = Review.objects.order_by("-created_on")
    template_name = "catalog/manage_reviews.html"


class EditBeerView(SuccessMessageMixin, generic.UpdateView):
    """
    View for editing an individual beer
    """
    model = Beer
    form_class = BeerForm
    template_name = "catalog/edit_beer.html"
    success_message = "The beer was edited successfully!"
    success_url = reverse_lazy("manage_beers")


class EditRequestView(SuccessMessageMixin, generic.UpdateView):
    """
    View for editing an individual beer
    """
    model = Requests
    form_class = RequestAdminForm
    template_name = "catalog/edit_request.html"
    success_message = "The request was edited successfully!"
    success_url = reverse_lazy("manage_requests")


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
            messages.add_message(request,
                                 messages.ERROR,
                                 'Error updating review!')

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
        messages.add_message(request,
                             messages.ERROR,
                             'You can only delete your own reviews!')

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
                'Request received - we will look into adding your beer shortly'
            )

    return render(
        request,
        "catalog/new_beer_request.html",
        {
            "request_form": request_form
        }
    )


def add_new_beer(request):
    beer_form = BeerForm()

    if request.method == "POST":
        beer_form = BeerForm(data=request.POST)
        if beer_form.is_valid():
            beer_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'New beer has successfully been added to the database!'
            )

    return render(
        request,
        "catalog/add_beer.html",
        {
            "beer_form": beer_form
        }
    )


def delete_beer(request, id):
    """
    View to delete beers
    """
    queryset = Beer.objects.all()
    beer = get_object_or_404(queryset, id=id)

    if request.user.is_staff:
        beer.delete()
        messages.add_message(request, messages.SUCCESS, 'Beer deleted!')
    else:
        messages.add_message(request,
                             messages.ERROR,
                             'You do not have permission to delete!')

    return HttpResponseRedirect(reverse('manage_beers'))


def post_request(request, id):
    """
    View to add requested beer to beer database
    """
    queryset = Requests.objects.all()
    beer_request = get_object_or_404(queryset, id=id)

    beer_form = BeerForm(data={
        "name": beer_request.beer_name,
        "tagline": f"""{beer_request.beer_name},
        Made by {beer_request.brewery_name},
        requested by {beer_request.user}""",
        "first_brewed": beer_request.first_brewed,
        "description": beer_request.comments,
        "beer_image": beer_request.image,
        "abv": beer_request.abv,
        "food_pairing": ["No pairings yet!",],
        "avg_rating": 0,
    })

    if beer_form.is_valid():
        beer_form.save()
        messages.add_message(
            request, messages.SUCCESS,
            'New beer has successfully been added to the database!'
            )
    else:
        messages.add_message(request,
                             messages.ERROR,
                             f'Invalid beer input. {beer_form.errors}')
        
    return HttpResponseRedirect(reverse('manage_requests'))


def delete_request(request, id):
    """
    View to delete requests
    """
    queryset = Requests.objects.all()
    beer_request = get_object_or_404(queryset, id=id)

    if request.user.is_staff:
        beer_request.delete()
        messages.add_message(request, messages.SUCCESS, 'Request deleted!')
    else:
        messages.add_message(request,
                             messages.ERROR,
                             'You do not have permission to delete!')

    return HttpResponseRedirect(reverse('manage_requests'))


def approve_review(request, id):
    """
    View to approve reviews as an admin
    """
    queryset = Review.objects.all()
    review = get_object_or_404(queryset, id=id)

    if request.user.is_staff:
        review.is_approved = True
        review.save()
        messages.add_message(request, messages.SUCCESS, 'Review approved!')
    else:
        messages.add_message(request,
                             messages.ERROR,
                             'You do not have permission to approve reviews!')
        
    return HttpResponseRedirect(reverse('manage_reviews'))


def delete_review(request, id):
    """
    View to delete reviews as an admin
    """
    queryset = Review.objects.all()
    review = get_object_or_404(queryset, id=id)

    if request.user.is_staff:
        review.delete()
        messages.add_message(request, messages.SUCCESS, 'Review deleted!')
    else:
        messages.add_message(request,
                             messages.ERROR,
                             'You do not have permission to delete!')

    return HttpResponseRedirect(reverse('manage_reviews'))
