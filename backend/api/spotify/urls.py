from django.urls import path, include
from . import views


urlpatterns = [
    path('redirect/', views.RedirectView.as_view()),
]
