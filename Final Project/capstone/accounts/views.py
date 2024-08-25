from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Patient
from hospitals.models import Hospital, Doctor


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("hospitals:index"))  # -----
        else:
            return render(request, "accounts/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("hospitals:index"))  # --


def register(request):
    hos = Hospital.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        is_doctor = request.POST["regi"] == "doc"
        is_patient = request.POST["regi"] == "pat"

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "accounts/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.is_doctor = is_doctor
            user.is_patient = is_patient
            user.save()

        except IntegrityError:
            return render(request, "accounts/register.html", {
                "message": "Username already taken."
            })

        if is_doctor:
            specialist = request.POST["specialist"]
            hospital = Hospital.objects.get(pk=request.POST["hospitals"])
            weeks = request.POST.getlist("weeks")
            week = ", ".join(weeks)
            fro = request.POST["from"]
            to = request.POST["to"]
            dc = Doctor.objects.create(user=user, hospital=hospital,
                                       specialization=specialist, weeks=week, fro=fro, to=to)
            dc.save()

        if is_patient:
            birth = request.POST["birth"]
            num = request.POST["number"]
            pt = Patient.objects.create(user=user, date_of_birth=birth, contact_number=num)
            pt.save()

        login(request, user)
        return HttpResponseRedirect(reverse("hospitals:index"))
    else:
        return render(request, "accounts/register.html", {
            "hospitals": hos
        })


@login_required
def editpro(request):
    dr = Doctor.objects.get(user=request.user)
    if request.method == "POST":
        dr.specialization = request.POST["specialist"]
        dr.hospital = Hospital.objects.get(pk=request.POST["hospitals"])
        weekss = request.POST.getlist("weeks")
        dr.weeks = ", ".join(weekss)
        dr.fro = request.POST["from"]
        dr.to = request.POST["to"]
        dr.save()
        return redirect("hospitals:index")
