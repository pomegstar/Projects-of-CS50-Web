from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create_list/", views.create_list, name="create_list"),
    path("categories/", views.categories, name="categories"),
    path("d_ca/<str:cate>/", views.d_ca, name="d_ca"),
    path("d_list/<int:id>/", views.d_list, name="d_list"),
    path("d_watchlist/", views.d_watchlist, name="d_watchlist"),
    path("comment/<int:id>/", views.comment, name="comment"),
    path("bids/<int:id>/", views.bids, name="bids"),
    path("close/<int:id>/", views.close, name="close"),
    path("mybids/", views.mybids, name="mybids")
]
