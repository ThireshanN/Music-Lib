import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.track import Track
from music.domainmodel.user import User

article_date = datetime.date(2020, 2, 28)


def insert_user(empty_session, values=None):
    new_id = 1
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (id, user_name, password) VALUES (:id, :user_name, :password)',
                          {'id': new_id, 'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (id, user_name, password) VALUES (:user_name, :password)',
                              {'id': value[0], 'user_name': value[1], 'password': value[2]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks (id, title, artist_id, album_id, url, duration, song_url) VALUES '
        '( 12, "tester", 12, 12, "http://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life/Food", 168,'
        '"https://files.freemusicarchive.org/storage-freemusicarchive-org/music/WFMU/AWOL/AWOL_-_A_Way_Of_Life/AWOL_-_03_-_Food.mp3")'
    )
    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]


def insert_artist(empty_session):
    new_id = 12
    full_name = "tester"
    empty_session.execute(
        'INSERT INTO artists (id, full_name) VALUES '
        '(12, "tester")')

    rows = list(empty_session.execute('SELECT id from artists'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_album(empty_session):
    empty_session.execute(
        'INSERT INTO albums (id, title) VALUES (12, "Tester")'
    )
    rows = list(empty_session.execute('SELECT id from albums'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (id, name) VALUES (12, "tester")'
    )
    rows = list(empty_session.execute('SELECT id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def make_track():
    return Track(12, "tester")


def make_album():
    return Album(12, "tester")


def make_artist():
    return Artist(12, "tester")


def make_genre():
    return Genre(12, "tester")


def make_user():
    return User(1, "Tester123", "Tester123")


def test_loading_of_user(empty_session):
    users = list()
    users.append((1, "Andrew", "1234"))
    users.append((2, "Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User(1, "Andrew", "1234"),
        User(2, "Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, user_name, password FROM users'))
    assert rows == [(1, "Tester123", "Tester123")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, (1, "Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(1, "Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_track(empty_session):
    track_key = insert_track(empty_session)
    expected_tracks = make_track()
    fetched_track = empty_session.query(Track).one()

    assert expected_tracks == fetched_track
    assert track_key == fetched_track.track_id


def test_load_of_artist(empty_session):
    artist_key = insert_artist(empty_session)
    expected_artist = make_artist()
    fetched_artist = empty_session.query(Artist).one()
    assert expected_artist == fetched_artist
    assert artist_key[0] == fetched_artist.artist_id


def test_load_of_album(empty_session):
    album_key = insert_album(empty_session)
    expected_album = make_album()
    fetched_album = empty_session.query(Album).one()

    assert expected_album == fetched_album
    assert album_key[0] == fetched_album.album_id


def test_load_of_genre(empty_session):
    genre_key = insert_genres(empty_session)
    expected_genre = make_genre()
    fetched_genre = empty_session.query(Genre).one()

    assert expected_genre == fetched_genre
    assert genre_key[0] == fetched_genre.genre_id

