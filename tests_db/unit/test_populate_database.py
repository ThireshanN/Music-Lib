from sqlalchemy import select, inspect

from music.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ["albums", "artists", "genres", "playlist", "playlist_tracks", "reviews",
                                           "tags", "track_genres", "tracks", "users"]


def test_database_populate_select_all_tracks(database_engine):
    inspector = inspect(database_engine)

    name_of_tracks_table = inspector.get_table_names()[8]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_tracks_table]])
        result = connection.execute(select_statement)

        all_tracks = []
        for row in result:
            all_tracks.append((row["id"], row["title"]))

        nr_tracks = len(all_tracks)
        assert nr_tracks == 2000

        assert all_tracks[0] == (2, "Food")


def test_database_populate_select_all_albums(database_engine):
    inspector = inspect(database_engine)

    name_of_albums_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_albums_table]])
        result = connection.execute(select_statement)

        all_albums = []

        for row in result:
            all_albums.append((row["id"], row["title"]))

        size_of_albums = len(all_albums)

        assert size_of_albums == 447
        assert all_albums[0] == (1, "AWOL - A Way Of Life")


def test_database_populate_select_all_artists(database_engine):
    inspector = inspect(database_engine)
    name_of_artist_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_artist_table]])
        result = connection.execute(select_statement)

        all_artist = []
        for row in result:
            all_artist.append((row["id"], row["full_name"]))

        number_of_artists = len(all_artist)
        assert number_of_artists == 263
        assert all_artist[0] == (1, "AWOL")


def test_database_populate_select_all_genres(database_engine):
    inspector = inspect(database_engine)
    name_of_genre_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_genre_table]])
        result = connection.execute(select_statement)

        all_genres = []
        for row in result:
            all_genres.append((row["id"], row["name"]))

        number_of_genres = len(all_genres)
        assert number_of_genres == 60

        assert all_genres[0] == (1, "Avant-Garde")


def test_database_populate_select_all_track_genres(database_engine):
    inspector = inspect(database_engine)
    name_of_genre_track_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_genre_track_table]])
        result = connection.execute(select_statement)
        all_track_genres = []
        for row in result:
            all_track_genres.append((row["track_id"], row["genre_id"]))
        list_length = len(all_track_genres)
        assert list_length == 60

        assert all_track_genres[0] == (155, 26)
