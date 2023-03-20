from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login', views.login_view),
    path('favicon.ico', views.favicon),
    path('register', views.register),
    path('logout', views.logout_view)
]
