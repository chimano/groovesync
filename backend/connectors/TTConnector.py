import requests
import os

api_key = os.environ['TT_API_KEY']
headers = {
    'client-secret': api_key
}
BASE_URL = 'https://conuhacks-playback-api.touchtunes.com/'


def get_artist_name(artist_id):
    r = requests.get(BASE_URL + 'artist/%s' %
                     (artist_id), headers=headers)
    return r.json()['artistTitle']


def get_song_name(tunes_id):
    r = requests.get(BASE_URL + 'song/%s' %
                     (tunes_id), headers=headers)
    return r.json()['songTitle']
