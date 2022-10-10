import pytest

import datetime

from sqlalchemy.exc import IntegrityError


article_date = datetime.date(2020, 2, 28)

def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks (id, title, artist_id, album_id, url, duration, song_url) VALUES '
        '( 1929192, "Tester_title", 12, 12, "http://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life/Food", 168, '
        '"https://files.freemusicarchive.org/storage-freemusicarchive-org/music/WFMU/AWOL/AWOL_-_A_Way_Of_Life/AWOL_-_03_-_Food.mp3")'
    )
    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]


#fuck knows how to write this