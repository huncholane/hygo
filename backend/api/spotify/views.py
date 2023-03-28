from rest_framework.views import APIView
from rest_framework.response import Response
from backend.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny


class RedirectView(APIView):
    sp_auth = SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
                           SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE)
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Redirects to Spotify's authorization page"""
        url = self.sp_auth.get_authorize_url()
        print(SPOTIFY_REDIRECT_URI)
        return Response({'redirect': url})

    def get(self, request):
        """Handles the redirect from Spotify's authorization page"""
        print(request.GET)
        print('Hello World')
        return Response('Hello World')
