import requests
import json
import mysql.connector

from settings import client_secret

BASE_URL = 'https://conuhacks-playback-api.touchtunes.com/'
REQUEST_HEADERS = {
    'client-secret': client_secret
}
OFFSET = 0

def getArtist(id):
    URL = BASE_URL + 'artist/%s' % (id)
    r = requests.get(URL, headers=REQUEST_HEADERS)
    return r

def getSong(id):
    URL + BASE_URL + 'song/%s' % (id)
    r = requests.get(URL, headers=REQUEST_HEADERS)
    return r
    
if __name__ == '__main__':
    URL = BASE_URL + 'plays?startDate=2018-02-19T21:00:00Z&endDate=2018-04-21T22:00:00Z&offset=%s' % (OFFSET)
    
    r = requests.get(URL,headers=REQUEST_HEADERS)

    location_songs = []
    # organize locations as keys tuple and dictionary of songs
    # for every location
    for p in r.json()['plays']:
        lat = p['latitude']
        lng = p['longitude']

        if lat < 45.703019 and lat > 45.357822:
            if lng > -74.071458 and lng < -73.216212:
                location_songs.append(p)
    print(location_songs)

        # location = (p['latitude'], p['longitude'])
        # if location in location_songs:
        #     location_songs[location].append(p)
        # else:
        #     location_songs[location] = [p]

    # add song and artist names to un-flattened dict
    # for l, val in location_songs.items():
    #     print(val)
    #     for s in val:
    #         artist = getArtist(s['artistId'])
    #         song = getSong(s['songId'])

