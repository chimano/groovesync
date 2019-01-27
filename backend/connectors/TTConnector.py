import requests

api_key = "9923ac9b-8fd3-421f-b0e5-952f807c6885"
headers = {
    'client-secret': api_key
}
BASE_URL = 'https://conuhacks-playback-api.touchtunes.com/'


def get_artist_name(artist_id):
    r = requests.get(BASE_URL + 'artist/%s' %
                     (artist_id), headers=headers)
    try:
        r.raise_for_status()
        return r.json()['artistTitle']
    except Exception as e:
        print(r.text)


def get_song_name(tunes_id):
    r = requests.get(BASE_URL + 'song/%s' %
                     (tunes_id), headers=headers)
    try:
        r.raise_for_status()
        return r.json()['songTitle']
    except Exception as e:
        print(r.text)
