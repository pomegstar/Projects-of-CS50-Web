from django.urls import path

from . import views

app_name = "hospitals"
urlpatterns = [
    path("", views.index, name="index"),
    path("hospital/<int:id>", views.doctors, name="doctors")
]
