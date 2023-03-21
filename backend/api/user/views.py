"""
User Views
"""
from .serializers import ListUserSerializer, SingleUserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ListUserSerializer

    def get_object(self):
        if self.kwargs['pk'] == 'me':
            return self.request.user
        return super().get_object()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'retrieve']:
            return SingleUserSerializer
        return ListUserSerializer

    @action(detail=True, methods=['get'])
    def isSpotifyToken(self, request, pk=None):
        user = self.get_object()
        return Response({'isSpotifyAuthorized': user.account.access_token is not None})
