from email.policy import default
from django.db import models
from django import forms
from django.contrib.auth.models import User
from spotipy import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
from backend.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_SCOPE
from .cache_handler import AccountCacheHandler

# Create your models here.


class Account(models.Model):
    private = models.BooleanField(default=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='account')
    access_token = models.CharField(max_length=255, null=True)
    refresh_token = models.CharField(max_length=255, null=True)
    token_expires_at = models.IntegerField(null=True)
    sp_id = models.CharField(null=True, max_length=30)

    @property
    def sp(self):
        cache_handler = AccountCacheHandler(self)
        sp_auth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
                               redirect_uri=SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE, cache_handler=cache_handler)
        return Spotify(auth_manager=sp_auth)

    def login_sp(self, code):
        cache_handler = AccountCacheHandler(self)
        sp_auth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
                               redirect_uri=SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE, cache_handler=cache_handler)
        sp_auth.get_access_token(code)
        return self.sp

    def __str__(self):
        return f'{self.user.username} Account'
