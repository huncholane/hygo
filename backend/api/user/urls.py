from rest_framework import routers
from .views import UserViewSet
from django.urls import path, include


router = routers.SimpleRouter()
router.register(r'', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
