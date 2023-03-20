from django.db import models
from home.models import Account

# Create your models here.


class Song(models.Model):
    uri = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    danceability = models.FloatField(default=0)
    valence = models.FloatField(default=0)
    energy = models.FloatField(default=0)
    tempo = models.FloatField(default=0)
    duration_ms = models.FloatField(default=0)
    loudness = models.FloatField(default=0)
    speechiness = models.FloatField(default=0)
    instrumentalness = models.FloatField(default=0)
    liveness = models.FloatField(default=0)
    acousticness = models.FloatField(default=0)
    image = models.CharField(max_length=255, null=True)


class Spotify(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    song_uri = models.CharField(max_length=200)
    num_plays = models.IntegerField(default=0)
    num_skips = models.IntegerField(default=0)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class Playlist(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    playlist_uri = models.CharField(max_length=200)
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=255)
    min_danceability = models.FloatField(default=0)
    max_danceability = models.FloatField(default=1)
    min_valence = models.FloatField(default=0)
    max_valence = models.FloatField(default=1)
    min_energy = models.FloatField(default=0)
    max_energy = models.FloatField(default=1)
    min_tempo = models.FloatField(default=0)
    max_tempo = models.FloatField(default=1)
    min_duration = models.FloatField(default=0)
    max_duration = models.FloatField(default=1000)
    min_loudness = models.FloatField(default=0)
    max_loudness = models.FloatField(default=1)
    min_speechiness = models.FloatField(default=0)
    max_speechiness = models.FloatField(default=1)
    min_instrumentalness = models.FloatField(default=0)
    max_instrumentalness = models.FloatField(default=1)
    min_liveness = models.FloatField(default=0)
    max_liveness = models.FloatField(default=1)
    min_acousticness = models.FloatField(default=0)
    max_acousticness = models.FloatField(default=1)
    play_to_skip_ratio = models.FloatField(default=1.5)
    followers = models.IntegerField(default=1)
    image = models.CharField(max_length=255, null=True)

    def songs(self):
        return (Spotify.objects.filter(account_id__in=self.friends())
                .values('song')
                .annotate(num_plays=models.Sum('num_plays'), num_skips=models.Sum('num_skips'))
                .filter(num_skips__lte=models.F('num_plays')/self.play_to_skip_ratio,
                        song__danceability__gte=self.min_danceability, song__danceability__lte=self.max_danceability,
                        song__valence__gte=self.min_valence, song__valence__lte=self.max_valence,
                        song__energy__gte=self.min_energy, song__energy__lte=self.max_energy,
                        song__duration_ms__gte=self.min_duration*1000, song__duration_ms__lte=self.max_duration*1000,
                        song__speechiness__gte=self.min_speechiness, song__speechiness__lte=self.max_speechiness,
                        song__instrumentalness__gte=self.min_instrumentalness, song__instrumentalness__lte=self.max_instrumentalness,
                        song__liveness__gte=self.min_liveness, song__liveness__lte=self.max_liveness,
                        song__acousticness__gte=self.min_acousticness, song__acousticness__lte=self.max_acousticness))

    def friends(self):
        return [friend.friend.id for friend in PlaylistFriend.objects.filter(playlist_id=self.id)]

    def length(self):
        return len(self.songs())

    def settings_dict(self):
        return {
            'danceability': [self.min_danceability, self.max_danceability],
            'valence': [self.min_valence, self.max_valence],
            'energy': [self.min_energy, self.max_energy],
            'duration_ms': [self.min_duration, self.max_duration],
            'speechiness': [self.min_speechiness, self.max_speechiness],
            'instrumentalness': [self.min_instrumentalness, self.max_instrumentalness],
            'liveness': [self.min_liveness, self.max_liveness],
            'acousticness': [self.min_acousticness, self.max_acousticness]
        }


"""This is a relation to a playlist that somebody wants to collaborate with friends on"""


class PlaylistFriend(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    friend = models.ForeignKey(Account, on_delete=models.CASCADE)
