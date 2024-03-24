from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Review


class ReviewList(generic.View):
    model = Review
    template_name = "users/all_reviews.html"


    def get(self, request, *args, **kwargs):
        
        if request.GET.get('query'):
            query = request.GET.get('query')
            if query in User.objects.values_list("username", flat=True):
                return redirect('user_reviews', query)
            else:
                messages.add_message(request, messages.ERROR, 'User does not exist!')
                return HttpResponseRedirect(reverse('all_reviews'))

        queryset = self.get_queryset()
        context = self.get_context_data(queryset)
        return render(
            request,
            self.template_name,
            context
        )


    def get_queryset(self):
        queryset = Review.objects.filter(is_approved=True).order_by("-created_on")
        return queryset
    
    
    def get_context_data(self, queryset):
        return {"review_list": queryset}


def user_reviews(request, username):
    """
    Display a users approved reviews from :model:`users.Review`.

    **Context**
    ``reviews``
        Entries in :model:`users.Reviewer` that have been approved.

    ** Template**
    :template:`users/user_reviews.html`
    """
    queryset = User.objects.all()
    user = get_object_or_404(queryset, username=username)
    reviews = user.reviewer.filter(is_approved=True).order_by("-created_on")
    reviews_count = reviews.count()

    context = {
        "user": user,
        "reviews": reviews,
        "reviews_count": reviews_count
    }

    return render(
        request,
        "users/user_reviews.html",
        context,
    )
