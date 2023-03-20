"""
Knox Urls
https://james1345.github.io/django-rest-knox/urls/
"""
from . import views, charts, public_playlsits
from .me import playlists
from django.urls import path, include


urlpatterns = [
    path('charts', charts.charts),
    path('charts/playlists', public_playlsits.public_playlists),
    path('charts/unpopular', charts.unpopular),
    path('queue', views.queue),
    path('me/playlsits', playlists.playlists),
    path('me/playlists/playlist', playlists.playlist),
    path('auth/', include('knox.urls'))
]
