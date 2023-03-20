from .hygo import get_sp, push_through_errors
from hygo.models import Playlist
import time

REST_TIME = 3600


def update_playlists_from_spotify():
    for playlist in Playlist.objects.all():
        sp = get_sp(playlist.account_id)
        playlist.num_songs = len(playlist.songs())
        data = push_through_errors(
            playlist.account_id, sp.playlist, playlist.playlist_uri)
        playlist.followers = data['followers']['total']
        playlist.image = data['images'][0]['url']
        playlist.save()


def update_playlists_loop():
    while True:
        time.sleep(REST_TIME)
        update_playlists_from_spotify()


def add_to_queue(account_id, track_id):
    sp = get_sp(account_id)
    push_through_errors(account_id, sp.add_to_queue, track_id)
