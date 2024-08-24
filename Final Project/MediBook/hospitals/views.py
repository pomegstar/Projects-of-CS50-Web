from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor, Hospital
from accounts.models import Patient, User
from appointments.models import Appointment


def index(request):
    hos = Hospital.objects.all()
    return render(request, "hospitals/hospitals.html", {
        "hospitals": hos,
    })


@login_required
def doctors(request, id):
    hos = Hospital.objects.get(pk=id)
    doct = Doctor.objects.filter(hospital=hos)
    return render(request, "hospitals/doctors.html", {
        "doctors": doct,
        "hosid": hos,
    })
