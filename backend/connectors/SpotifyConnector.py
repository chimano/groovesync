import requests
import base64
import datetime
import json
import os

client_id = os.environ['SPOTIFY_CLIENT_ID']
secret_id = os.environ['SPOTIFY_SECRET_ID']
AUTH_URL = 'https://accounts.spotify.com/'
API_URL = 'https://api.spotify.com/'
acquired_at = datetime.datetime.now()
auth_headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Authorization': base64.b64encode('%s:%s' % (client_id, secret_id))
}

MAX_LIMIT = 20


def refresh_token():
    r = requests.post(AUTH_URL + 'api/token', headers=auth_headers,
                      data={'grant_type': 'client_credentials'})
    return r.json()['access_token']


access_token = refresh_token()
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Authorization': "Bearer %s" % (access_token)
}


def search_song(song_name, artist_name):
    try:
        r = requests.get(API_URL + "v1/search",
                         params={"q": "name:" + song_name,
                                 "type": "track"},
                         headers=headers)
        if r.status_code == 401:
            new_access_token = refresh_token()
            headers['Authorization'] = "Bearer %s" % new_access_token
            r = requests.get(API_URL + "v1/search",
                             params={"q": "name:" + song_name,
                                     "type": "track"},
                             headers=headers)

        r.raise_for_status()
        response_dict = json.loads(r.text)
        for track in response_dict:
            for artist in track['artists']:
                if artist['name'].lower() == artist_name.lower():
                    return track['id']
    except Exception as e:
        print("Failed to find song", e)
    return -1


def get_song_features(ids):
    features = {}
    for i in range(0, len(ids), MAX_LIMIT):
        batched_ids = ids[i:i + MAX_LIMIT]
        try:
            r = requests.get(API_URL + "v1/audio-features",
                             params={'ids': ','.join(batched_ids)},
                             headers=headers)
            if r.status_code == 401:
                new_access_token = refresh_token()
                headers['Authorization'] = "Bearer %s" % new_access_token
                r = requests.get(API_URL + "v1/audio-features",
                                 params={'ids': ','.join(batched_ids)},
                                 headers=headers)
            r.raise_for_status()
            response_dict = json.loads(r.text)
            features = {**features, **dict(zip(batched_ids, response_dict['audio_features']))}
        except Exception as e:
            print("Something went wrong with the features", e)
            return -1

    return features
