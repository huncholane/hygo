from django.shortcuts import render


def playlists(request):
    return render(request, 'me/playlists.html')
