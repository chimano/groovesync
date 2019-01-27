import requests
import json
import matplotlib.pyplot as plt
from settings import client_secret
from datetime import datetime

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
    location_songs = { }

    for OFFSET in range(0,6085877, 5000):
        URL = BASE_URL + \
            'plays?startDate=2018-11-19T21:00:00Z&endDate=2018-12-30T22:00:00Z&offset=%s&limit=5000' % (
                OFFSET)
        r = requests.get(URL, headers=REQUEST_HEADERS)
        print(OFFSET)
        
        # organize locations as keys tuple and dictionary of songs
        # for every location
        for p in r.json()['plays']:
            lat = p['latitude']
            lng = p['longitude']

            location = (p['latitude'], p['longitude'])
            if location in location_songs:
                #check for uniqueness
                if p['songId'] in location_songs[location]:
                    delta = datetime.strptime(p['playDate'], "%Y-%m-%dT%H:%M:%S.%f%z") - datetime.strptime(location_songs[location][p['songId']][1], "%Y-%m-%dT%H:%M:%S.%f%z")
                    if delta.total_seconds() > 180:
                        c = location_songs[location][p['songId']]
                        new_c = (c[0]+1, p['playDate'], c[2])
                        location_songs[location][p['songId']]= new_c
                elif p['songId'] not in location_songs[location]:
                    location_songs[location][p['songId']] = (1, p['playDate'], p['artistId']) 
            else:
                location_songs[location] = { p['songId']: (1, p['playDate'], p['artistId'])}
    
    with open('out.log', 'w') as file:
        file.write(location_songs)
