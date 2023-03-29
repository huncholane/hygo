from django.urls import path
from . import views


urlpatterns = [
    path('', views.LogView.as_view(), name='logs'),
]
