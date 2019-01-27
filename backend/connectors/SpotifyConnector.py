import requests
import base64
import datetime
import json
import os


client_id = os.environ['SPOTIFY_CLIENT_ID']
secret_id = os.environ['SPOTIFY_SECRET_ID']
AUTH_URL = 'https://accounts.spotify.com/'
API_URL = 'https://api.spotify.com/'
access_token = refresh_token()
acquired_at = datetime.datetime.now()
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Authorization': "Bearer %s" % (access_token)
}
auth_headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Authorization': base64.b64encode('%s:%s' % (client_id, secret_id))
}

MAX_LIMIT = 20


def refresh_token():

    r = requests.post(AUTH_URL + 'api/token', headers=auth_headers,
                      data={'grant_type': 'client_credentials'})
    return r['access_token']
    auth_headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': base64.b64encode('%s:%s' % (client_id, secret_id))
    }


def search_song(song_name, artist_name):
    r = requests.get(API_URL + "v1/search",
                     params={"q": "name:" + song_name,
                               "type": "track"},
                     headers=headers)
    if r.status_code == 401:
        access_token = refresh_token()
        global headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': "Bearer %s" % (access_token)
        }
        return search_song(song_name, artist_name)

    response_dict = json.loads(r.text)
    for track in response_dict:
        for artist in track['artists']:
            if artist['name'].lower() == artist_name.lower():
                return track['id']

    return -1


def get_song_features(ids, user_token=None):
    features = []
    for i in range(0, len(ids), MAX_LIMIT):
        batched_ids = ids[i:i+MAX_LIMIT]
        try:
            r = requests.get(API_URL + "v1/audio-features",
                             params={'ids': ','.join(batched_ids)},
                             headers=headers)

            response_dict = json.loads(r.text)
            features += response_dict['audio_features']
            if r.status_code == 401:
                global headers = {
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Authorization': "Bearer %s" % (access_token)
                }
                access_token = refresh_token()
                return get_song_features(song_name, artist_name)
        except:
            print("Something went wrong with the features")
            break
            return -1

    return features
