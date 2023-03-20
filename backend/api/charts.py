from django.http import JsonResponse
from django.shortcuts import render
from hygo.models import Spotify, Song
from django.db.models import Count, Sum, F
from sp_conn.song_data import get_songs


def charts(request):
    num_songs = 50
    items = (Spotify.objects
             .values('song_id')
             .annotate(Users=Count('account_id'), Skips=Sum('num_skips'), Listens=Sum('num_plays'), valid=Sum('num_skips')*2)
             .filter(valid__lte=F('Listens'))
             .order_by(*['-Users', '-Listens', 'Skips'])
             )[:num_songs]
    return get_songs(items)


def unpopular(request):
    num_songs = 50
    items = (Spotify.objects
             .values('song_id')
             .annotate(Users=Count('account_id'), Skips=Sum('num_skips'), Listens=Sum('num_plays'), valid=Sum('num_skips')*2)
             .filter(valid__gte=F('Listens'))
             .order_by(*['-Users', '-Listens', '-Skips'])
             )[:num_songs]
    return get_songs(items)


def get_songs(items):
    data = []
    for i, item in enumerate(items):
        song = Song.objects.get(id=item['song_id'])
        uri = song.uri
        name = song.name+' - '+song.artist
        image = song.image
        data.append([
            i+1,
            f'''<button class="btn" onclick="queue(this)" uri="{uri}" ><img height="38.5" src="{image}"> {name}</button>''',
            item['Skips'],
            item['Listens'],
            item['Users']
        ])
    headings = ['#', 'Song', 'Skips', 'Listens', 'Users']
    return JsonResponse({
        'perPage': 50,
        'data': {
            'headings': headings,
            'data': data
        }
    })
