from db import session
from ast import literal_eval
from models import Songs, Artists, Locations, Plays
from sqlalchemy.sql.expression import ClauseElement


def create_if_not_exists(model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return
    else:
        params = dict((k, v) for k, v in kwargs.items()
                      if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return


def main(input_file):
    with open(input_file, 'r') as file:
        tt_data = literal_eval(file.read())
    for loc in tt_data:
        currrent_loc = Locations(loc[0], loc[1])
        session.add(currrent_loc)
        session.flush()

        song_dict = tt_data[loc]
        for song_id in song_dict:
            count = song_dict[song_id][0]
            artist_id = song_dict[song_id][2]
            create_if_not_exists(Artists, id=artist_id)
            create_if_not_exists(Songs, tunes_id=song_id, artist_id=artist_id)

            session.refresh(currrent_loc)
            current_play = Plays(currrent_loc.id, song_id, count)
            session.add(current_play)

    session.commit()
