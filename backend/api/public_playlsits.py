from django.http import JsonResponse
from hygo.models import Playlist


def public_playlists(request):
    headers = ['#', 'Playlist', 'User', 'Follows', 'Songs']
    items = Playlist.objects.filter(
        account__private=False)
    items = sorted(items, key=lambda x: (-x.followers, -x.length()))
    data = []
    for i, item in enumerate(items):
        data.append([
            i+1,
            f'<img height="40" src="{item.image}"> <a href="{item.playlist_uri}">{item.name}</a>',
            item.account.user.username,
            item.followers,
            len(item.songs())
        ])
    return JsonResponse({
        'data': {
            'headings': headers,
            'data': data
        }
    })
