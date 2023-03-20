from spotipy.cache_handler import CacheHandler


class AccountCacheHandler(CacheHandler):
    def __init__(self, account, *args, **kwargs):
        self.account = account

    def get_cached_token(self):
        return {
            'access_token': self.account.access_token,
            'expires_at': self.account.token_expires_at,
            'refresh_token': self.account.refresh_token,
        }

    def save_token_to_cache(self, token_info):
        self.account.access_token = token_info['access_token']
        self.account.refresh_token = token_info['refresh_token']
        self.account.token_expires_at = token_info['expires_at']
        self.account.save()
