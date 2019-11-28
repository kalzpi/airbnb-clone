from django.views.generic import ListView, DetailView
from . import models


class HomeView(ListView):

    """ Homeview Difinition """

    model = models.Room

    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"


class RoomDetail(DetailView):
    model = models.Room
