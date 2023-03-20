from django.http import JsonResponse
from hygo.models import Playlist, Song
from home.models import Account
from django.forms.models import model_to_dict


def playlists(request):
    account_id = Account.objects.get(user_id=request.user.id).id
    playlists = Playlist.objects.filter(account_id=account_id).order_by('id')
    playlist_data = []
    for playlist in playlists:
        playlist_data.append(model_to_dict(playlist))
    return JsonResponse({
        'playlists': playlist_data
    })


def playlist(request):
    playlist_id = request.GET['playlist_id']
    playlist = Playlist.objects.get(id=playlist_id)
    songs = playlist.songs()
    chart_data = {
        'perPage': len(songs),
        'data': {
            'headings': ['Song', 'Skips', 'Plays'],
            'data': []
        }
    }
    for item in songs:
        song = Song.objects.get(id=item['song'])
        num_skips = item['num_skips']
        num_plays = item['num_plays']
        uri = song.uri
        chart_data['data']['data'].append([
            f'<button class="btn" onclick="queue(this)" uri="{uri}" ><img src="{song.image}" height="38.5"> {song.name} - {song.artist}</button>',
            num_skips,
            num_plays
        ])
    return JsonResponse({
        'settings': playlist.settings_dict(),
        'chart': chart_data
    })
