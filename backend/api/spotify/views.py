from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from backend.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
from spotipy.oauth2 import SpotifyOAuth
from spotipy.client import Spotify
from django.shortcuts import redirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import login


class RedirectView(APIView):
    sp_auth = SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
                           SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE)
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Redirects to Spotify's authorization page"""
        url = self.sp_auth.get_authorize_url()
        if request.user != AnonymousUser():
            login(request, request.user)
        return Response({'redirect': url})

    def get(self, request):
        """Handles the redirect from Spotify's authorization page"""
        code = request.GET.get('code')
        if request.user != AnonymousUser():
            request.user.account.login_sp(code)
        else:
            print('no user')
            access_token = self.sp_auth.get_access_token(code)
            sp = Spotify(access_token['access_token'])
            # print(access_token)
        return redirect('/user/login')
