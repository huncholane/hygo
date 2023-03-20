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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, null=True)
    refresh_token = models.CharField(max_length=255, null=True)
    token_expires_at = models.IntegerField(null=True)

    @property
    def sp(self):
        cache_handler = AccountCacheHandler(self)
        sp_auth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
                               redirect_uri=SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE, cache_handler=cache_handler)
        return Spotify(auth_manager=sp_auth)

    def __str__(self):
        return f'{self.user.username} Account'
