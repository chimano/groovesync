import requests
import base64
import datetime
import json


class SpotifyConnector:
    def __init__(self, client_id, secret_id, user_token=None):

        self.AUTH_URL = 'https://accounts.spotify.com/'
        self.API_URL = 'https://api.spotify.com/'
        self.access_token = self.refresh_token()
        self.acquired_at = datetime.datetime.now()
        self.headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': "Bearer %s" % (self.access_token)}

        self.MAX_LIMIT = 20

    def refresh_token(self):
        auth_headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': base64.b64encode('%s:%s' % (client_id, secret_id))}
        }

        r = requests.post(self.AUTH_URL + 'api/token', headers=auth_headers,
                          data = {'grant_type': 'client_credentials'})
        return r['access_token']


    def search_song(self, song_name, artist_name):
        r=requests.get(self.API_URL + "v1/search",
                    params={"q":"name:" + song_name,
                            "type": "track"},
                    headers=self.headers)
        
        response_dict = json.loads(r.text)
        for track in response_dict:
            for artist in track['artists']:
                if artist['name'].lower() == artist_name.lower():
                    return track['id']
        
        return -1


    def get_song_features(self, ids):
        features = []
        for i in range(0, len(ids), self.MAX_LIMIT):
            batched_ids = ids[i:i+self.MAX_LIMIT]
            try:

                r = requests.get(self.API_URL + "v1/audio-features", 
                            params={'ids':','.join(batched_ids)},
                            headers=self.headers)
                        
                response_dict = json.loads(r.text)
                features += response_dict['audio_features']
            except:
                print("Something went wrong with the features")
                return -1

        return features
