from django.urls import path, re_path, include
from . import views

app_name = "mony"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
