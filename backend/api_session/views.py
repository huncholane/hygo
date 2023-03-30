from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout, authenticate

# Create your views here.


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response('OK')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed()
        login(request, user)
        return Response('OK')


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response('OK')
