from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float

Base = declarative_base()


class Testtable(Base):
    __tablename__ = 'testtable'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50))

    def __init__(self, name):
        self.name = name


class Songs(Base):
    __tablename__ = 'songs'
    tunes_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    spotify_id = Column(Integer)
    name = Column(String(50), nullable=True)
    mode = Column(Integer)
    acousticness = Column(Float)
    danceability = Column(Float)
    energy = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    loudness = Column(Float)
    speechiness = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)

    def __init__(self, tunes_id, artist_id):
        self.tunes_id = tunes_id
        self.artist_id = artist_id


class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)
    mode = Column(Integer)
    acousticness = Column(Float)
    danceability = Column(Float)
    energy = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    loudness = Column(Float)
    speechiness = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)

    def __init__(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude


class Plays(Base):
    __tablename__ = 'plays'
    id = Column(Integer, primary_key=True)
    location_id = Column(
        Integer, ForeignKey("locations.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.tunes_id"), nullable=False)
    count = Column(Integer)

    def __init__(self, location_id, song_id, count):
        self.location_id = location_id
        self.song_id = song_id
        self.count = count


class Artists(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)

    def __init__(self, id):
        self.id = id
