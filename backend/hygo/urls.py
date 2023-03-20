from django.urls import path
from . import views

urlpatterns = [
    path('', views.hygo),
    path('manage', views.manage),
    path('playlistboard', views.playlistboard),
    path('game', views.game)
]
