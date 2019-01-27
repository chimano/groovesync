from db import session
from models import Songs, Artists
from connectors.SpotifyConnector import search_song, get_song_features


def main(args):
    songs = session.query(Songs)
    artists = session.query(Artists)
    for song in songs.all():
        song.spotify_id = search_song(song.name, artists.filter_by(id=song.artist_id).first().name)
    session.flush()

    songs = session.query(Songs)
    song_ids = list(songs.values(Songs.spotify_id))
    features_by_id = get_song_features(song_ids)
    for song in songs:
        if not song.spotify_id not in features_by_id:
            continue
        f = features_by_id[song.spotify_id]
        song.mode = f["mode"]
        song.acousticness = f["acousticness"]
        song.danceability = f["danceability"]
        song.energy = f["energy"]
        song.instrumentalness = f["instrumentalness"]
        song.liveness = f["liveness"]
        song.loudness = f["loudness"]
        song.speechiness = f["speechiness"]
        song.valence = f["valence"]
        song.tempo = f["tempo"]
    session.flush()
