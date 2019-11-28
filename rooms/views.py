from django.urls import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView
from . import models


class HomeView(ListView):

    """ Homeview Difinition """

    model = models.Room

    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        print(vars(room))
        return render(request, "rooms/detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        # return redirect(reverse("core:home"))
        raise Http404()
