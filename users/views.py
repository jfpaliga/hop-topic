from django.shortcuts import render
from django.contrib import messages

from .forms import RequestsForm


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
        "users/new_beer_request.html",
        {
            "request_form": request_form
        }
    )
