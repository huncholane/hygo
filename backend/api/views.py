from django.http import HttpResponse
from django.shortcuts import render
from sp_conn.playlist_data import add_to_queue
from home.models import Account
from django.contrib.auth.decorators import login_required


# Create your views here.


def queue(request):
    if not request.user.is_authenticated:
        return HttpResponse('unauthorized')
    uri = request.GET['uri']
    account_id = Account.objects.get(user_id=request.user.id).id
    add_to_queue(account_id, uri)
    return HttpResponse('OK')
