from rest_framework.views import APIView
from rest_framework.response import Response
from backend.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User


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
        code = request.GET.get('code')
        print(request.user)
        user = User.objects.get(username='huncho')
        print(code)
        sp = user.account.login_sp(code)
        # print(sp.me())
        return Response(code)
