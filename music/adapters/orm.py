from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapper
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

track_table = Table(
    "tracks", metadata,  # This is the name of the table we are creating
    Column("id", Integer, primary_key=True, autoincrement=False),
    Column("title", String(255), nullable=False),
    Column("artist_id", ForeignKey("artists.id")),
    Column("album_id", ForeignKey("albums.id")),
    Column("url", String(255), nullable=False),
    Column("duration", String(255), nullable=False),
    Column("song_url", String(255), nullable=False)
)

artist_table = Table(
    "artists", metadata,
    Column("id", Integer, primary_key=True, autoincrement=False),
    Column("full_name", String(255), nullable=False),

)


album_table = Table(
    "albums", metadata,
    Column("id", Integer, primary_key=True, autoincrement=False),
    Column("title", String(255), nullable=False),
    Column("url", String(255), nullable=False),
    Column("type", String(255), nullable=False),
    Column("release_year", Integer, nullable=False),

)

genres_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=False),
    Column("name", String(255), nullable=False)
)

# don't think we need this.
tags_table = Table(
    "tags", metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False)
)

reviews_table = Table(
    "reviews", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("rating", Integer, nullable=False),
    Column("review_text", String(1024), nullable=False),
    Column("timestamp", DateTime, nullable=False)
)

track_genre_table = Table(
    'track_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.id')),
    Column('genre_id', ForeignKey('genres.id'))
)


def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__user_id': users_table.c.id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        #'_User__reviews': relationship(User.Review, backref='_Comment__user')
    })  # Above needs to be the relationship between user and review -> Not working

    mapper(Genre, genres_table, properties={
        "_Genre__genre_id": genres_table.c.id,
        "_Genre__name": genres_table.c.name
    })

    mapper(Artist, artist_table, properties={
        "_Artist__artist_id": artist_table.c.id,
        "_Artist__full_name": artist_table.c.full_name
    })

    mapper(Album, album_table, properties={
        "_Album__album_id": album_table.c.id,
        "_Album__title": album_table.c.title,
        "_Album__album_url": album_table.c.url,
        "_Album__album_type": album_table.c.type,
        "_Album__release_year": album_table.c.release_year
    })

    mapper(Track, track_table, properties={
        "__track_id": track_table.c.id,
        "_Track__title": track_table.c.title,
        "_Track__track_url": track_table.c.url,
        "_Track__track_duration": track_table.c.duration,
        "_Track__song_url": track_table.c.song_url,
        "_Track__genres": relationship(Genre, secondary=track_genre_table) # Not sure if this is correct
    })

    mapper(Review, reviews_table, properties={
        "_Review__review_text": reviews_table.c.review_text,
        "_Review__rating": reviews_table.c.rating,
        "_Review__timestamp": reviews_table.c.timestamp
    })
