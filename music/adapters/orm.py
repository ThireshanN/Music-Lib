from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapper

from music.domainmodel import user, genre, artist, album, track, review, playlist


# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=False),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

track_table = Table(
    "tracks", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255), nullable=False),
    Column("artist_id", ForeignKey("artists.id")),
    Column("album_id", ForeignKey("albums.id")),
    Column("url", String(255), nullable=True),
    Column("duration", String(255), nullable=True),
    Column("song_url", String(255), nullable=True)
)

artist_table = Table(
    "artists", metadata,
    Column("id", Integer, primary_key=True),
    Column("full_name", String(255), nullable=False),

)

album_table = Table(
    "albums", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255), nullable=False),
    Column("url", String(255), nullable=True),
    Column("type", String(255), nullable=True),
    Column("release_year", Integer, nullable=True)
)
playlist_table = Table(
    'playlist', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True)
)

genres_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True),
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

playlist_tracks_table = Table(
    'playlist_tracks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column("playlist_id", ForeignKey("playlist.id")),
    Column('track_id', ForeignKey('tracks.id'))
)


def map_model_to_tables():
    mapper(user.User, users_table, properties={
        '_User__user_id': users_table.c.id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password
    })

    mapper(track.Track, track_table, properties={
        "_Track__track_id": track_table.c.id,
        "_Track__title": track_table.c.title,
        "_Track__artist": relationship(artist.Artist),
        "_Track__album": relationship(album.Album),
        "_Track__track_url": track_table.c.url,
        "_Track__track_duration": track_table.c.duration,
        "_Track__song_url": track_table.c.song_url,
        "_Track__genres": relationship(
            genre.Genre,
            secondary=track_genre_table,
            back_populates='_Genre__tracks'),
        "_Track__playlists_added_to": relationship(
            playlist.PlayList,
            secondary=playlist_tracks_table,
            back_populates='_Playlist__tracks')
    })  # Don't think that genres are working correctly

    mapper(album.Album, album_table, properties={
        "_Album__album_id": album_table.c.id,
        "_Album__title": album_table.c.title,
        "_Album__album_url": album_table.c.url,
        "_Album__album_type": album_table.c.type,
        "_Album__release_year": album_table.c.release_year
    })

    mapper(artist.Artist, artist_table, properties={
        "_Artist__artist_id": artist_table.c.id,
        "_Artist__full_name": artist_table.c.full_name
    })

    mapper(genre.Genre, genres_table, properties={
        "_Genre__genre_id": genres_table.c.id,
        "_Genre__name": genres_table.c.name,
        "_Genre__tracks": relationship(
            track.Track,
            secondary=track_genre_table,
            back_populates='_Track__genres')
    })

    mapper(review.Review, reviews_table, properties={
        "_Review__review_text": reviews_table.c.review_text,
        "_Review__rating": reviews_table.c.rating,
        "_Review__timestamp": reviews_table.c.timestamp
    })

    mapper(playlist.PlayList, playlist_table, properties={
        "_Playlist__playlist_id": playlist_table.c.id,
        "_Playlist__tracks": relationship(
            track.Track,
            secondary=playlist_tracks_table,
            back_populates='_Track__playlists_added_to')
    })
