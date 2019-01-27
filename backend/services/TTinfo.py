from connectors.TTConnector import get_song_name, get_artist_name
from db import session
from models import Songs, Artists


def main():
    songs = session.query(Songs).all()

    for song in songs:
        song_name = get_song_name(song.tunes_id)
        song.name = song_name

    session.commit()

    artists = session.query(Artists).all()

    for artist in artists:
        artist_name = get_artist_name(artist.id)
        artist.name = artist_name

    session.commit()
