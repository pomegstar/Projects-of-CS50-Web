from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entries, name="entries"),
    path("search/", views.search, name="search"),
    path("random/", views.rand, name="random"),
    path("new/", views.new, name="new"),
    path("edit/", views.edit, name="edit"),
    path("s_edit/", views.s_edit, name="s_edit")
]
