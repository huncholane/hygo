from django.urls import path
from . import views

urlpatterns = [
    path('', views.charts),
    path('playlists', views.public_playlists),
    path('unpopular', views.unpopular)
]
