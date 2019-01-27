from db import session
from out import tt_data
from models import Songs, Artists, Locations, Plays
from sqlalchemy import ClauseElement


def get_or_create(model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems()
                      if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


for loc in tt_data:
    currrent_loc = Locations(loc[0], loc[1])
    session.add(currrent_loc)
    session.flush()

    song_dict = tt_data[loc]
    for song_id in song_dict:
        count = song_dict[song_id][0]
        artist_id = song_dict[song_id][2]
        current_artist, _ = get_or_create(Artists, id=artist_id)
        current_song, _ = get_or_create(
            Songs, tunes_id=song_id, artist_id=artist_id)

        session.refresh(currrent_loc)
        current_play = Plays(currrent_loc.id, song_id, count)


session.commit()
