import requests


class TTConnector:
    def __init__(self, api_key):
        self.headers = {
            'client-secret': api_key
        }
        self.BASE_URL = 'https://conuhacks-playback-api.touchtunes.com/'

    def get_artist_name(self, artist_id):
        r = requests.get(self.BASE_URL + 'artist/%s' %
                         (artist_id), headers=self.headers)
        return r.json()['artistTitle']

    def get_song_name(self, tunes_id):
        r = requests.get(self.BASE_URL + 'song/%s' %
                         (tunes_id), headers=self.headers)
        return r.json()['songTitle']
