import django
from django.shortcuts import render, redirect, HttpResponse
from home.models import Account
from hygo.models import Playlist, PlaylistFriend
import sp_conn.song_data
import sp_conn.hygo

import json
# Create your views here.


def playlistboard(request):
    data = {}
    if 'account' in request.session:
        data['account'] = request.session['account']
    else:
        return redirect('../login')
    if request.method == 'GET':
        playlists = Playlist.objects.all()
        sp = get_sp(2)
        sorted_playlists = []
        for i, playlist in enumerate(playlists):
            p = push_through_errors(
                data['account']['id'], sp.playlist, playlist.playlist_uri)
            sp = get_sp(playlist.account_id)
            setattr(playlist, 'username', Account.objects.get(
                id=playlist.account_id).username)
            setattr(playlist, 'rank', i)
            setattr(playlist, 'followers', p['followers']['total'])
            sorted_playlists.append(playlist)
        data['playlists'] = sorted(
            sorted_playlists, key=lambda x: -getattr(x, 'followers'))
        return render(request, 'hygo/playlistboard.html', data)


def manage(request):
    if 'account' not in request.session:
        return redirect('../login')
    data = {'account': request.session['account']}
    if request.method == 'GET':
        playlists = Playlist.objects.filter(account_id=data['account']['id'])
        for playlist in playlists:
            setattr(playlist, 'friends', ','.join([
                str(pf.friend_id) for pf in PlaylistFriend.objects.filter(playlist_id=playlist.id)]))
        data['playlists'] = playlists
        authorized = get_authorized_account_ids()
        authorized.remove(data['account']['id'])
        accounts = Account.objects.filter(id__in=authorized)
        data['accounts'] = accounts
        return render(request, 'hygo/manage.html', data)
    if request.method == 'POST':
        d = json.load(request)
        if d['delete']:
            print('Delete', d['uri'])
            delete_hygo(data['account']['id'], d['uri'])
        elif d['uri'] == 'new':
            print('Create new playlist')
            create_hygo(data['account']['id'], d['name'],
                        d['desc'], d['chosenFriends'], d['mindanceability'],
                        d['maxdanceability'], d['minvalence'], d['maxvalence'],
                        d['minenergy'], d['maxenergy'], d['mintempo'],
                        d['maxtempo'], d['minduration'], d['maxduration'],
                        d['minloudness'], d['maxloudness'], d['minspeechiness'],
                        d['maxspeechiness'], d['mininstrumentalness'],
                        d['maxinstrumentalness'], d['minliveness'],
                        d['maxliveness'], d['minacousticness'], d['maxacousticness'])
        else:
            print('Update playlist', d['uri'])
            update_hygo(data['account']['id'], d['uri'], d['name'],
                        d['desc'], d['chosenFriends'], d['mindanceability'],
                        d['maxdanceability'], d['minvalence'], d['maxvalence'],
                        d['minenergy'], d['maxenergy'], d['mintempo'],
                        d['maxtempo'], d['minduration'], d['maxduration'],
                        d['minloudness'], d['maxloudness'], d['minspeechiness'],
                        d['maxspeechiness'], d['mininstrumentalness'],
                        d['maxinstrumentalness'], d['minliveness'],
                        d['maxliveness'], d['minacousticness'], d['maxacousticness'])
        return HttpResponse('ok')


def hygo(request):
    data = {}
    if 'account' in request.session:
        data['account'] = request.session['account']
    else:
        return redirect('../login')
    if request.method == 'GET':
        code = request.GET.get('code', None)
        if is_cached(data['account']['id']):
            users = Account.objects.filter(id__in=get_authorized_account_ids())
            data['users'] = users
            data['home'] = True
            data['songs'] = django_cnx.query(
                'SELECT * FROM sp_performance WHERE num_users > 1 AND num_plays > num_skips*2 ORDER BY num_users DESC, num_skips, num_plays DESC LIMIT 50')
            song_uris = [x['song_uri'] for x in data['songs']]
            sp = get_sp(2)
            songs = sp.tracks(song_uris)['tracks']
            for i, song in enumerate(data['songs']):
                data['songs'][i]['name'] = songs[i]['name']
                data['songs'][i]['artist'] = ', '.join(
                    [s['name'] for s in songs[i]['artists']])
                data['songs'][i]['image'] = songs[i]['album']['images'][2]['url']
        elif code is None:
            data['needs_auth'] = True
        else:
            get_token(data['account']['id'], code)
            listen_to_user(data['account']['id'])
            return redirect('.')
        return render(request, 'hygo/index.html', data)
    if request.method == 'POST':
        # Do spotify login magic and add to db
        sp_auth = get_auth(data['account']['id'])
        print(sp_auth.get_authorize_url())
        return redirect(sp_auth.get_authorize_url())


def game(request):
    data = {}
    if 'account' not in request.session:
        return redirect('../login')
    data['account'] = request.session['account']
    data['accounts'] = Account.objects.filter(
        private=False, id__in=get_authorized_account_ids())
    ids = [str(x.id) for x in data['accounts']]
    query = '('+', '.join(ids)+')'
    uri = django_cnx.query(
        f'SELECT * FROM hygo_spotify WHERE account_id IN {query} ORDER BY RAND() LIMIT 1')[0]['song_uri']
    song = django_cnx.query(
        'SELECT * FROM hygo_spotify WHERE song_uri = %s ORDER BY num_plays DESC LIMIT 1', uri)[0]
    correct = django_cnx.query(
        'SELECT username FROM home_account WHERE `id` = %s', song['account_id'])[0]
    data['song'] = song
    songs = get_sp(2).tracks([song['song_uri'].split(':')[-1]])
    data['song']['name'] = songs['tracks'][0]['name']
    data['song']['image'] = songs['tracks'][0]['album']['images'][1]['url']
    data['correct'] = correct
    print(song, correct)
    return render(request, 'hygo/game.html', data)


def play(request):
    data = {}
    if 'account' not in request.session:
        return redirect('../login')
    data['account'] = request.session['account']
    return HttpResponse('OK')
