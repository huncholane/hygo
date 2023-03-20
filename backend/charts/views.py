from django.shortcuts import render

# Create your views here.


def charts(request):
    return render(request, 'charts/index.html')


def public_playlists(request):
    return render(request, 'charts/public_playlists.html')


def unpopular(request):
    return render(request, 'charts/unpopular.html')
