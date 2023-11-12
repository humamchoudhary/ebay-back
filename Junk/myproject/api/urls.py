from django.urls import path

from . import views

urlpatterns = [
    path("",views.getData),
    path("getUsers",views.getUsers),
    path("login",views.postUserLogin),
    path("signup",views.postUserSignup),
]