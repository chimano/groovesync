import os
from connectors.TTConnector import TTConnector
from db import session
from models import Songs, Artists
api_key = os.environ['TT_API']

tt_connector = TTConnector(api_key)

songs = session.query(Songs).all()

for song in songs:
    song_name = tt_connector.get_song_name(song.tunes_id)
    song.name = song_name

session.commit()

artists = session.query(Artists).all()

for artist in artists:
    artist_name = tt_connector.get_artist_name(artist.id)
    artist.name = artist_name

session.commit()
