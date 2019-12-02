from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):

    """ Homeview Difinition """

    model = models.Room

    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"


class RoomDetail(DetailView):
    model = models.Room


def search(request):

    city = request.GET.get("city")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    s_amenities = request.GET.getlist("amenities")
    s_amenities = list(map(int, s_amenities))  # s_amenities는 list를 int화 하였다.
    s_facilities = request.GET.getlist("facilities")  # s_facilitiy는 int를 string화 하였다.
    instant = request.GET.get("instant", False)
    superhost = request.GET.get("superhost", False)

    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "s_price": price,
        "s_guests": guests,
        "s_bedrooms": bedrooms,
        "s_beds": beds,
        "s_baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    if room_type != 0:
        filter_args["room_type"] = room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant:
        filter_args["instant_book"] = True

    if superhost:
        filter_args["host__superhost"] = True

    filter_args["country"] = country

    print(s_amenities)

    if s_amenities:
        filter_args["amenities__pk__in"] = s_amenities

    if s_facilities:
        filter_args["facility__pk__in"] = s_facilities

    rooms = models.Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms},)
