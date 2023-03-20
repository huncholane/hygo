from django.urls import path
from . import playlists

urlpatterns = [
    path('playlists', playlists.playlists)
]
