import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse

from .models import User, Posts, Follow, Like


def index(request):
    posts = Posts.objects.all()
    psts = posts.order_by("-timestamp").all()
    paginator = Paginator(psts, 10)
    page_num = request.GET.get('page')
    pstPage = paginator.get_page(page_num)

    liked_posts = []
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(
            liker=request.user).values_list('liked_post_id', flat=True)

    for post in pstPage:
        post.like_count = Like.objects.filter(liked_post=post).count()


    return render(request, "network/index.html", {
        "posts": psts,
        "title": "All Posts",
        "paginPost": pstPage,
        "liked": liked_posts,
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":
        newpost = request.POST["post"]
        posts = Posts(
            poster=request.user,
            post=newpost
        )
        posts.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/newpost.html")



@csrf_exempt
def profile(request, id):
    pstr = User.objects.get(pk=id)
    posts = Posts.objects.filter(poster=pstr)
    psts = posts.order_by("-timestamp").all()
    paginator = Paginator(psts, 10)
    page_num = request.GET.get('page')
    pstPage = paginator.get_page(page_num)
    isFlwing = False
    liked_posts = []
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(
            liker=request.user).values_list('liked_post_id', flat=True)

    for post in pstPage:
        post.like_count = Like.objects.filter(liked_post=post).count()

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("follow") is not None:
            if data["follow"]:
                if not Follow.objects.filter(usr=request.user, follower=pstr).exists():
                    f = Follow(usr=request.user, follower=pstr)
                    f.save()
                    isFlwing = True
            else:
                if Follow.objects.filter(usr=request.user, follower=pstr).exists():
                    d = Follow.objects.get(usr=request.user, follower=pstr)
                    d.delete()
                    isFlwing = False
            following = Follow.objects.filter(usr=pstr)
            follower = Follow.objects.filter(follower=pstr)
            return JsonResponse({
                'success': True,
                'following': following.count(),
                'follower': follower.count(),
                'isFollowing': isFlwing
            }, status=200)

    else:
        if request.user.is_authenticated:
            if Follow.objects.filter(usr=request.user, follower=pstr).exists():
                isFlwing = True
            else:
                isFlwing = False
        following = Follow.objects.filter(usr=pstr)
        follower = Follow.objects.filter(follower=pstr)
        return render(request, "network/index.html", {
            "posts": psts,
            "title": f"Profile of {pstr.username}",
            "paginPost": pstPage,
            "pro": pstr,
            "following": following,
            "follower": follower,
            "isFollowing": isFlwing,
            "liked": liked_posts
        })


@login_required
def following(request):
    flw = request.user
    flwing = Follow.objects.filter(usr=flw)
    posts = Posts.objects.all()
    psts = posts.order_by("-timestamp").all()

    flwingpst = []
    for post in psts:
        for person in flwing:
            if person.follower == post.poster:
                flwingpst.append(post)

    paginator = Paginator(flwingpst, 10)
    page_num = request.GET.get('page')
    pstPage = paginator.get_page(page_num)

    liked_posts = []
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(
            liker=request.user).values_list('liked_post_id', flat=True)

    for post in pstPage:
        post.like_count = Like.objects.filter(liked_post=post).count()

    return render(request, "network/index.html", {
        "title": "Following",
        "paginPost": pstPage,
        "liked": liked_posts
    })


@csrf_exempt
@login_required
def edit(request, id):
    if request.method == "PUT":
        pst = Posts.objects.get(pk=id)
        data = json.loads(request.body)
        if data.get("edited") is not None:
            pst.post = data["edited"]
            pst.save()
    return HttpResponse(status=204)


@csrf_exempt
@login_required
def liking(request, id):
    if request.method == "PUT":
        pst = Posts.objects.get(pk=id)
        data = json.loads(request.body)
        if data.get("like") is not None:
            if data["like"]:
                if not Like.objects.filter(liker=request.user, liked_post=pst).exists():
                    l = Like(liker=request.user, liked_post=pst)
                    l.save()
            else:
                if Like.objects.filter(liker=request.user, liked_post=pst).exists():
                    ul = Like.objects.get(liker=request.user, liked_post=pst)
                    ul.delete()
            liked = Like.objects.filter(liked_post=pst)
            return JsonResponse({
                'liked': liked.count(),
            }, status=200)
