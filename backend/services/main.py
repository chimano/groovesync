import requests
import json

from settings import client_secret

if __name__ == '__main__':
    URL =  'https://conuhacks-playback-api.touchtunes.com/plays?startDate=2018-02-19T21:00:00Z&endDate=2018-02-19T22:00:00Z&offset=0'
    headers = {
        'client-secret': client_secret
    }
    r = requests.get(URL,headers=headers).json()
    print(r)
