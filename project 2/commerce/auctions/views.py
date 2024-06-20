from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, A_listing, Comments, Bids


def index(request):
    active_listing = A_listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "active": active_listing,
        "subtitle": "Active Listings",
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_list(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        img_url = request.POST["img_url"]
        price = request.POST["price"]
        owner = request.user
        category = Category.objects.get(pk=int(request.POST["category"]))
        bid = Bids(bid=int(price), bidder=owner)
        bid.save()
        n_listing = A_listing(title=title, description=description,
                              image_url=img_url, price=bid, owner=owner, category=category)
        n_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_list.html", {
            "owners": User.objects.all(),
            "categories": Category.objects.all()
        })


def categories(request):
    cate = A_listing.objects.values_list("category", flat=True)
    # listing = listing.category.all()
    ca = []
    for categ in cate:
        n = Category.objects.get(pk=categ)
        if n not in ca:
            ca.append(n)

    return render(request, "auctions/category.html", {
        "categories": ca,
        "category": Category,
    })


def d_ca(request, cate):
    ac = Category.objects.get(categoryName=cate)
    act = ac.category.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "active": act,
        "subtitle": f"Active listings of {cate}",
    })


def d_list(request, id):
    list = A_listing.objects.get(pk=id)
    is_in_watchlist = request.user in list.watchlist.all()
    cmnt = Comments.objects.filter(listing=list)
    isowner = request.user.username == list.owner.username
    if request.method == "POST":
        listing = A_listing.objects.get(pk=int(request.POST["lis"]))
        add_watchlist = request.POST["addwatch"] == "True"
        if add_watchlist:
            listing.watchlist.add(request.user)
            # watch = list.watchlist.add(list)
            return render(request, "auctions/details.html", {
                "listing": listing,
                "iswatch": request.user in list.watchlist.all(),
                "comments": cmnt,
                "isowner": isowner
            })

        else:
            listing.watchlist.remove(request.user)
            return render(request, "auctions/details.html", {
                "listing": listing,
                "iswatch": request.user in list.watchlist.all(),  # add_watchlist
                "comments": cmnt,
                "isowner": isowner
            })

    return render(request, "auctions/details.html", {
        "listing": list,
        "iswatch": is_in_watchlist,
        "comments": cmnt,
        "isowner": isowner
    })


@login_required
def d_watchlist(request):
    c_user = request.user
    w_list = c_user.watch.all()
    return render(request, "auctions/index.html", {
        "active": w_list,
        "subtitle": f"Watchlist of {c_user}"
    })


@login_required
def comment(request, id):
    list = A_listing.objects.get(pk=id)
    coment = request.POST["comment"]
    c_user = request.user
    cmnt = Comments(comment=coment, commentor=c_user, listing=list)
    cmnt.save()
    return HttpResponseRedirect(reverse("d_list", args=(id, )))


@login_required
def bids(request, id):
    try:
        list = A_listing.objects.get(pk=id)
        cmnt = Comments.objects.filter(listing=list)
        isowner = request.user.username == list.owner.username
        bidder = request.user
        bid = int(request.POST["bid"])
        if bid > list.price.bid:
            n_bid = Bids(bid=bid, bidder=bidder, blist=list)
            n_bid.save()
            list.price = n_bid
            list.save()
            return render(request, "auctions/details.html", {
                "listing": list,
                "iswatch": request.user in list.watchlist.all(),  # add_watchlist
                "comments": cmnt,
                "isowner": isowner,
                "message": "Your bid is successful."
            })
        else:
            return render(request, "auctions/details.html", {
                "listing": list,
                "iswatch": request.user in list.watchlist.all(),  # add_watchlist
                "comments": cmnt,
                "isowner": isowner,
                "message": "Your bid is failed, because of low price."
            })
    except Exception:
        return render(request, "auctions/details.html", {
                "listing": list,
                "iswatch": request.user in list.watchlist.all(),  # add_watchlist
                "comments": cmnt,
                "isowner": isowner,
                "message": "Something wrong!"
            })


@login_required
def close(request, id):
    list = A_listing.objects.get(pk=id)
    cmnt = Comments.objects.filter(listing=list)
    isowner = request.user.username == list.owner.username
    list.is_active = False
    list.save()
    return render(request, "auctions/details.html", {
        "listing": list,
        "iswatch": request.user in list.watchlist.all(),  # add_watchlist
        "comments": cmnt,
        "isowner": isowner,
        "mssage": "Auction is closed."
    })

@login_required
def mybids(request):
        c_user = request.user
        mybids= Bids.objects.filter(bidder=c_user)
        return render(request, "auctions/bids.html", {
            "bids": mybids,
            "subtitle": "My Bids",
            })
