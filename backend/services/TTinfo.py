from connectors.TTConnector import get_song_name, get_artist_name
from db import session
from models import Songs, Artists


def main(args):
    offset = int(args[0])
    start = int(args[1])
    songs = session.query(Songs).all()

    i = 1
    for song in list(songs)[start::offset]:
        i = i + 1
        song_name = get_song_name(song.tunes_id)
        song.name = song_name
        if i % 10 == 0:
            print(i)

    session.commit()

    artists = session.query(Artists).all()

    for artist in list(artists)[start::offset]:
        i = i + 1
        artist_name = get_artist_name(artist.id)
        artist.name = artist_name
        if i % 10 == 0:
            print(i)

    session.commit()
