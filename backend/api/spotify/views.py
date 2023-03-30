from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from backend.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
from spotipy.oauth2 import SpotifyOAuth
from spotipy.client import Spotify
from django.shortcuts import redirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import login
from home.models import Account
import string
import random


def random_string(len):
    return ''.join(random.choices(string.ascii_letters+string.digits, k=len))


def create_sp_user(me, access_token):
    next_id = User.objects.order_by('-id').first().id+1
    username = random_string(10) + str(next_id)
    first_name, last_name = me['display_name'].split()
    user = User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=random_string(20)
    )
    account = Account.objects.create(
        user=user,
        sp_id=me['id'],
        access_token=access_token['access_token'],
        refresh_token=access_token['refresh_token'],
        token_expires_at=access_token['expires_at']
    )


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
            access_token = self.sp_auth.get_access_token(code)
            sp = Spotify(access_token['access_token'])
            me = sp.me()
            query = User.objects.filter(account__sp_id=me['id'])
            if query:
                user = query.first()
            else:
                user = create_sp_user(me, access_token)
            login(request, user)
        return redirect('/user')
