from db import session
from models import Songs, Artists
from connectors.SpotifyConnector import search_song


def main():
    song_details = session.query(Songs).join()
    for song_name, artist_name in song_details:
        search_song(song_name, artist_name)
