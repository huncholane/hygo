import os
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify, util
import time
from requests.exceptions import ConnectionError
from urllib3.exceptions import MaxRetryError, ReadTimeoutError

cache_dir = os.path.join(os.path.dirname(__file__), 'sp_cache')
if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)
scope = 'ugc-image-upload user-modify-playback-state user-read-playback-state user-read-currently-playing playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private app-remote-control streaming user-library-modify user-library-read'
SLEEP_TIME = 10


def push_through_errors(account_id, func, *args, **kwargs):
    while True:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(account_id, e)
            time.sleep(SLEEP_TIME)


def get_authorized_account_ids():
    cached = os.listdir(cache_dir)
    authorized = []
    for c in cached:
        authorized.append(int(c.split('-')[1]))
    return authorized


def is_cached(account_id):
    return os.path.exists(os.path.join(cache_dir, f'.cache-{account_id}'))


def get_token(account_id, code=None):
    sp_auth = get_auth(account_id)
    token_data = sp_auth.get_access_token(code=code)
    token = token_data['access_token']
    return token


def get_auth(account_id):
    return SpotifyOAuth(
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        username=account_id,
        cache_path=os.path.join(cache_dir, f'.cache-{account_id}')
    )


def get_sp(account_id):
    sp = Spotify(auth_manager=get_auth(account_id))
    sp.account_id = account_id
    return sp
