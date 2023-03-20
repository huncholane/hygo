from threading import Thread
from home.models import Account
import datetime
from hygo.models import Spotify as SP, Playlist, PlaylistFriend, Song
import time
import os
import base64
from django.db.models import Sum
from . import song_data
from .auth import get_sp, cache_dir, is_cached, push_through_errors

LOOP_TIME = 10
AFK_TIME = 60
CANCEL_SKIP = 15
DESCRIPTION = 'This hype ghost keeps track of your favorite songs. It all starts at hygo.io and can merge with friends.'


def listen_to_user(account_id):

    def listen():
        sp = get_sp(account_id)
        me = push_through_errors(account_id, sp.me)
        print('Listening to account', account_id,
              Account.objects.get(id=account_id).user.username, me['display_name'])
        data = push_through_errors(account_id, sp.current_playback)
        # Get the first song on starting up
        while data is None or 'item' not in data or data['item'] is None or 'id' not in data['item']:
            time.sleep(AFK_TIME)
            data = push_through_errors(account_id, sp.current_playback)
        data['unskipped'] = False
        last_data = data.copy()
        while True:
            data = push_through_errors(account_id, sp.current_playback)
            if data is None or 'item' not in data or data['item'] is None or 'id' not in data['item']:
                time.sleep(AFK_TIME)
                continue
            if len(SP.objects.filter(account_id=account_id, song__uri=data['item']['uri'])) == 0 or last_data['item']['uri'] != data['item']['uri']:
                print(f'getting new song for {account_id}')
                add_new_listen(data, account_id)
                manage_user_playlists(account_id)
                data['unskipped'] = False
            else:
                data['unskipped'] = last_data['unskipped']
            data['time_left'] = data['item']['duration_ms'] - \
                data['progress_ms']
            if data['time_left'] <= CANCEL_SKIP*1000 and not data['unskipped']:
                data['unskipped'] = True
                print(
                    f'unskipping {data["item"]["uri"]} for {Account.objects.get(id=account_id).user.username}')
                listen_data = list(SP.objects.filter(
                    account_id=account_id, song__uri=data['item']['uri']))[0]
                num_skips = max([listen_data.num_skips, 1])
                SP.objects.filter(account_id=account_id, song__uri=data['item']['uri']).update(
                    num_skips=num_skips-1)
            last_data = data.copy()
            time.sleep(LOOP_TIME)
    Thread(target=listen, daemon=True).start()


def add_new_listen(data, account_id):
    if len(Song.objects.filter(uri=data['item']['uri'])) == 0:
        song = song_data.download_song(data['item']['uri'])
    else:
        song = Song.objects.get(uri=data['item']['uri'])
    if len(SP.objects.filter(account_id=account_id, song__uri=data['item']['uri'])) == 0:
        SP.objects.create(account_id=account_id, song_id=song.id)
    listen_data = list(SP.objects.filter(
        account_id=account_id, song__uri=data['item']['uri']))[0]
    SP.objects.filter(account_id=account_id, song__uri=data['item']['uri']).update(
        num_plays=listen_data.num_plays+1, num_skips=listen_data.num_skips+1)


def search_playlist(account_id, name):
    potential = Account.objects.filter(id=account_id)[0]
    if potential.playlist_id is not None:
        return potential.playlist_id
    sp = get_sp(account_id)
    playlists = push_through_errors(account_id, sp.current_user_playlists)
    for playlist in playlists['items']:
        if playlist['name'] == name:
            return playlist['uri']


def create_hygo(account_id, name, desc=DESCRIPTION, friends=[], min_danceability=0, max_danceability=1, min_valence=0, max_valence=1, min_energy=0, max_energy=1,
                min_tempo=0, max_tempo=400, min_duration=0, max_duration=1000, min_loudness=0, max_loudness=1, min_speechiness=0, max_speechiness=1,
                min_instrumentalness=0, max_instrumentalness=1, min_liveness=0, max_liveness=1, min_acousticness=0, max_acousticness=1):
    if desc == '':
        desc = DESCRIPTION
    sp = get_sp(account_id)
    me = push_through_errors(account_id, sp.me)['id']
    print('creating playlist for', account_id)
    playlist = create_playlist(account_id, me, name, desc)
    p = Playlist(account_id=account_id, name=name, desc=desc, min_danceability=min_danceability, max_danceability=max_danceability, min_valence=min_valence,
                 max_valence=max_valence, min_energy=min_energy, max_energy=max_energy, min_tempo=min_tempo, max_tempo=max_tempo, min_duration=min_duration,
                 max_duration=max_duration, min_loudness=min_loudness, max_loudness=max_loudness, min_speechiness=min_speechiness, max_speechiness=max_speechiness,
                 min_instrumentalness=min_instrumentalness, max_instrumentalness=max_instrumentalness, min_liveness=min_liveness, max_liveness=max_liveness,
                 min_acousticness=min_acousticness, max_acousticness=max_acousticness, playlist_uri=f"spotify:playlist:{playlist['id']}")
    p.save()
    for friend in friends:
        pf = PlaylistFriend(playlist_id=p.id, friend_id=friend)
        pf.save()
    img = get_logo()
    upload_cover_image_to_playlist(account_id, playlist['id'], img)
    manage_user_playlist(p)
    return playlist['id']


def delete_hygo(account_id, playlist_uri):
    sp = get_sp(account_id)
    push_through_errors(account_id, sp.current_user_unfollow_playlist,
                        playlist_uri.split(':')[-1])
    playlist = Playlist.objects.get(playlist_uri=playlist_uri)
    PlaylistFriend.objects.filter(playlist_id=playlist.id).delete()
    playlist.delete()


def update_hygo(account_id, playlist_uri, name, desc=DESCRIPTION, friends=[], min_danceability=0, max_danceability=1, min_valence=0, max_valence=1, min_energy=0, max_energy=1,
                min_tempo=0, max_tempo=400, min_duration=0, max_duration=1000, min_loudness=0, max_loudness=1, min_speechiness=0, max_speechiness=1,
                min_instrumentalness=0, max_instrumentalness=1, min_liveness=0, max_liveness=1, min_acousticness=0, max_acousticness=1):
    if desc == '':
        desc = DESCRIPTION
    sp = get_sp(account_id)
    me_id = push_through_errors(account_id, sp.me)['id']
    playlist_id = playlist_uri.split(':')[-1]
    push_through_errors(account_id, sp.user_playlist_change_details, me_id,
                        playlist_id, name=name, description=desc)
    p = Playlist.objects.get(playlist_uri=playlist_uri)
    Playlist.objects.filter(playlist_uri=playlist_uri).update(min_danceability=min_danceability, max_danceability=max_danceability, min_valence=min_valence,
                                                              max_valence=max_valence, min_energy=min_energy, max_energy=max_energy, min_tempo=min_tempo, max_tempo=max_tempo, min_duration=min_duration,
                                                              max_duration=max_duration, min_loudness=min_loudness, max_loudness=max_loudness, min_speechiness=min_speechiness, max_speechiness=max_speechiness,
                                                              min_instrumentalness=min_instrumentalness, max_instrumentalness=max_instrumentalness, min_liveness=min_liveness, max_liveness=max_liveness,
                                                              min_acousticness=min_acousticness, max_acousticness=max_acousticness)
    PlaylistFriend.objects.filter(playlist_id=p.id).delete()
    for friend in friends:
        pf = PlaylistFriend(playlist_id=p.id, friend_id=friend)
        pf.save()
    manage_user_playlist(p)


def upload_cover_image_to_playlist(account_id, playlist_id, img):
    sp = get_sp(account_id)
    return push_through_errors(account_id, sp.playlist_upload_cover_image, playlist_id, img)


def create_playlist(account_id, me_id, name, desc):
    sp = get_sp(account_id)
    return push_through_errors(account_id, sp.user_playlist_create, me_id, name, description=desc)


def update_metadata(account_id):
    sp = get_sp(account_id)
    playlist_id = search_playlist(account_id, 'Hygo')
    img = get_logo()
    upload_cover_image_to_playlist(account_id, playlist_id, img)
    push_through_errors(account_id, sp.playlist_change_details,
                        playlist_id, name=Account.objects.get(id=account_id).user.username.capitalize()+' Hygo', description=DESCRIPTION)


def get_logo():
    with open(f'{cache_dir}/../../ghostsystems/static/background/inverted2048x2048.jpg', 'rb') as f:
        return base64.b64encode(f.read())


def update_playlist_images():
    for playlist in Playlist.objects.all():
        upload_cover_image_to_playlist(
            playlist.account.id, playlist.playlist_uri.split(':')[-1], get_logo())


def get_playlist_song_ids(account_id, me, playlist_id):
    songs = []
    sp = get_sp(account_id)
    data = push_through_errors(account_id,
                               sp.user_playlist_tracks, me, playlist_id, limit=100)
    songs += data['items']
    while data['next'] is not None:
        data = push_through_errors(account_id,
                                   sp.next, data)
        songs += data['items']
    song_ids = []
    for song in songs:
        song_ids.append('spotify:track:'+song['track']['id'])
    return song_ids


def manage_user_playlists(account_id):
    account = Account.objects.filter(id=account_id)[0]
    playlists = Playlist.objects.filter(account_id=account_id)
    for playlist in playlists:
        manage_user_playlist(playlist)
    if len(playlists) == 0:
        print(f'Creating the default hygo for {account.user.username}')
        create_hygo(account_id, f'{account.user.username.capitalize()} Hygo')


def manage_user_playlist(playlist):
    account = Account.objects.filter(id=playlist.account_id)[0]
    sp = get_sp(playlist.account_id)
    me = push_through_errors(playlist.account_id, sp.me)['id']
    song_ids = get_playlist_song_ids(
        playlist.account_id, me, playlist.playlist_uri)
    tracks = []
    account_ids = [playlist.account_id]
    [account_ids.append(pf.friend_id)
     for pf in PlaylistFriend.objects.filter(playlist_id=playlist.id)]
    for item in SP.objects.filter(account_id__in=account_ids).values('song__uri').annotate(num_skips=Sum('num_skips'), num_plays=Sum('num_plays')):
        if item['num_skips'] == 0 or item['num_plays']/item['num_skips'] > 1.5:
            tracks.append(item['song__uri'])
    db_track_features = get_track_features(playlist.account_id, tracks)
    tracks = get_ids_for_playlist_criteria(db_track_features, playlist)
    pl_track_features = get_track_features(playlist.account_id, song_ids)
    song_ids = get_ids_for_playlist_criteria(pl_track_features, playlist)
    remove_songs = list(set(song_ids).difference(set(tracks)))
    add_songs = list(set(tracks).difference(set(song_ids)))
    for i in range(0, len(add_songs), 100):
        print(
            f'Adding {add_songs} for {account.user.username}')
        push_through_errors(playlist.account_id, sp.playlist_add_items,
                            playlist.playlist_uri, add_songs[i:i+100], position=0)
    for i in range(0, len(remove_songs), 100):
        print(
            f'Removing {remove_songs} for {account.user.username}')
        push_through_errors(playlist.account_id,
                            sp.playlist_remove_all_occurrences_of_items, playlist.playlist_uri, remove_songs[i:i+100])


def get_ids_for_playlist_criteria(tracks, playlist):
    ids = []
    for track in tracks:
        if (playlist.min_acousticness <= track['acousticness'] <= playlist.max_acousticness and
            playlist.min_danceability <= track['danceability'] <= playlist.max_danceability and
            playlist.min_duration*1000 <= track['duration_ms'] <= playlist.max_duration*1000 and
            playlist.min_energy <= track['energy'] <= playlist.max_energy and
            playlist.min_instrumentalness <= track['instrumentalness'] <= playlist.max_instrumentalness and
            playlist.min_liveness <= track['liveness'] <= playlist.max_liveness and
            playlist.min_speechiness <= track['speechiness'] <= playlist.max_speechiness and
            playlist.min_tempo <= track['tempo'] <= playlist.max_tempo and
                playlist.min_valence <= track['valence'] <= playlist.max_valence):
            ids.append(track['id'])
    return ids


def get_track_features(account_id, tracks):
    """Converts list of track ids to tracks with audio features"""
    sp = get_sp(account_id)
    advanced = []
    for i in range(0, len(tracks), 100):
        advanced.extend(push_through_errors(account_id, sp.audio_features,
                                            tracks[i:i+100]))
    return advanced


def replace_playlist_tracks(playlist_id, account_id, me, tracks):
    sp = get_sp(account_id)
    push_through_errors(account_id, sp.user_playlist_replace_tracks,
                        me, playlist_id, tracks)


def load_listeners():
    for account in Account.objects.all():
        if is_cached(account.id):
            listen_to_user(account.id)


def reset_listens(account_id):
    SP.objects.filter(id=account_id).update(num_plays=0, num_skips=0)


def play_song(account_id, song_uri):
    pass


# load_listeners()
