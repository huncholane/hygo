from .auth import get_sp, push_through_errors
from hygo.models import Spotify, Song
from django.db.models import Count


def get_songs(track_ids):
    data = []
    max = 50
    for i in range(0, len(track_ids), max):
        sp = get_sp(2)
        songs = push_through_errors(2, sp.tracks, track_ids[i:i+max])['tracks']
        for song in songs:
            try:
                image = song['album']['images'][0]['url']
            except:
                pass
            data.append({
                'name': song['name'],
                'artist': song['artists'][0]['name'],
                'image': image,
                'duration_ms': song['duration_ms']
            })
    return data


def get_features(track_ids):
    data = []
    max = 50
    for i in range(0, len(track_ids), max):
        sp = get_sp(2)
        songs = push_through_errors(
            2, sp.audio_features, track_ids[i:i+max])
        data.extend(songs)
    return data


def get_missing_songs():
    downloaded_songs = [song.uri for song in Song.objects.all()]
    missing = (Spotify.objects.values('song_uri')
               .annotate(num_users=Count('song_uri'))
               .exclude(song_uri__in=downloaded_songs))
    return [song['song_uri'] for song in missing]


def download_songs(track_ids):
    datas = get_songs(track_ids)
    features = get_features(track_ids)
    songs = []
    for uri, data, feature in zip(track_ids, datas, features):
        if feature == None:
            song = dict(
                uri=uri, name=data['name'], artist=data['artist'], image=data['image'])
        else:
            song = dict(uri=uri, name=data['name'], artist=data['artist'], danceability=feature['danceability'],
                        valence=feature['valence'], energy=feature['energy'], tempo=feature['tempo'],
                        duration_ms=feature['duration_ms'], loudness=feature['loudness'], speechiness=feature['speechiness'],
                        instrumentalness=feature['instrumentalness'], liveness=feature['liveness'],
                        acousticness=feature['acousticness'], image=data['image'])
        if len(Song.objects.filter(uri=uri)) == 0:
            song = Song(**song)
            song.save()
            print('Saving', song.name, 'for the first time')
        else:
            Song.objects.filter(uri=uri).update(**song)
            song = Song.objects.get(uri=uri)
            print('Updating data for', song.name)
        songs.append(song)
    return songs


def download_song(song_uri):
    return download_songs([song_uri])[0]
