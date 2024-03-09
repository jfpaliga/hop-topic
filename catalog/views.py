from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Beer, Review
from .forms import ReviewForm

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


def edit_review(request, id, review_id):
    """
    view to edit reviews
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
    view to delete reviews
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
