from connectors.TTConnector import get_song_name, get_artist_name
from db import session
from models import Songs, Artists, Plays


def main(args):
    plays = session.query(Plays).all()
    plays_by_loc = {}
    for play in plays:
        if play.location_id not in plays_by_loc:
            plays_by_loc[play.location_id] = []
        plays_by_loc[play.location_id].append((play.count, play.song_id))
    plays_by_loc = {k: sorted(v, key=lambda x: x[0], reverse=True)[:50] for k, v in plays_by_loc.items()}
    print(len(plays_by_loc), len(plays_by_loc[3]))
    song_ids = set()
    for p in plays_by_loc.values():
        song_ids.update([e[1] for e in p])

    songs = session.query(Songs).filter(Songs.tunes_id.in_(song_ids))
    i = 1
    for song in songs.all():
        i = i + 1
        song_name = get_song_name(song.tunes_id)
        song.name = song_name
        if i % 10 == 0:
            print(i)

    session.flush()
    artist_ids = list(v[0] for v in songs.values(Songs.artist_id))
    artists = session.query(Artists).filter(Artists.id.in_(artist_ids))

    for artist in artists.all():
        i = i + 1
        artist_name = get_artist_name(artist.id)
        artist.name = artist_name or ''
        if i % 10 == 0:
            print(i)

    session.commit()
