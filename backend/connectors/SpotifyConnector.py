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

    def refresh_token(self):
        auth_headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': base64.b64encode('%s:%s' % (client_id, secret_id))}
        }

        r = requests.post(self.AUTH_URL + 'api/token', headers=auth_headers,
                          data = {'grant_type': 'client_credentials'})
        return r['access_token']

    def search_song(self, song_name, artist_name):
        formatted_name=song_name.replace(' ', '%20')
        r=requests.get(self.API_URL + "v1/search?name:%s&type=track" % (formatted_name),
                       headers=self.headers)
        
        response_dict = json.loads(r.text)
        for track in 
