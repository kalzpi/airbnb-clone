from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import models

# Create your views here.
# Important point of Queryset: Queryset is lazy. It doesn't load all of information from DB when you call some_set.object.all(), it will be done when you actually USE it.


def all_rooms(request):
    page = request.GET.get(
        "page", 1
    )  # get_page에서 page로 변경하며 default값인 1을 지정해줄 필요가 생겼다.
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)

    try:
        rooms = paginator.page(
            page
        )  # get_page는 max_page 이상의 값이 url에 입력되어도 자동으로 last page를 보여주는 exception handling이 포함되었으나, page에는 그러한 기능이 없어 EmptyPage 에러를 호출한다.
        return render(request, "rooms/home.html", {"page": rooms})
    except (EmptyPage, PageNotAnInteger):
        # rooms = paginator.page(
        #     1
        # )  # 이것은 EmptyPage 오류가 발생했을 때 대신 paginator instance가 가져온 1페이지를 보여준다. 그러나 url은 여전히 잘못 입력된 상태이다.
        return redirect("/")  # 1페이지만 보여주는 대신, home.html로 redirect 시키는 기능

    # print(vars(rooms))  # Paginator가 models.Room.objects.all에서 무엇을 가져왔는지 보자.
    # print(vars(rooms.paginator))  # Paginator가 준 paginator instance에는 무엇이 들어있는지 보자.

    # return render(request, "rooms/home.html", {"page": rooms}) #EmptyPage error를 handling 하기위해 위 try문 안으로 위치가 이동되었다.
