import ast
import csv
from pathlib import Path
from datetime import date, datetime

from werkzeug.security import generate_password_hash

from music.adapters.csvdatareader import TrackCSVReader
from music.adapters.repository import AbstractRepository
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.track import Track


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        # Read first line of the the CSV file.
        headers = next(reader)
        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def create_track_object(track_row):
    track = Track(int(track_row['track_id']), track_row['track_title'])
    track.track_url = track_row['track_url']
    track_duration = round(float(
        track_row['track_duration'])) if track_row['track_duration'] is not None else None
    if type(track_duration) is int:
        track.track_duration = track_duration
    return track


def create_artist_object(track_row):
    artist_id = int(track_row['artist_id'])
    artist = Artist(artist_id, track_row['artist_name'])
    return artist


def create_album_object(row):
    album_id = int(row['album_id'])
    album = Album(album_id, row['album_title'])
    album.album_url = row['album_url']
    album.album_type = row['album_type']

    album.release_year = int(
        row['album_year_released']) if row['album_year_released'].isdigit() else None

    return album


def extract_genres(track_row: dict):
    # List of dictionaries inside the string.
    track_genres_raw = track_row['track_genres']
    # Populate genres. track_genres can be empty (None)
    genres = []
    if track_genres_raw:
        try:
            genre_dicts = ast.literal_eval(
                track_genres_raw) if track_genres_raw != "" else []

            for genre_dict in genre_dicts:
                genre = Genre(
                    int(genre_dict['genre_id']), genre_dict['genre_title'])
                genres.append(genre)
        except Exception as e:
            print(track_genres_raw)
            print(f'Exception occurred while parsing genres: {e}')

    return genres


def load_tracks(data_path: Path, repo: AbstractRepository, database_mode: bool):
    print("Getting to load tracks in the data_importer")
    track_reader = TrackCSVReader(str(data_path / "raw_albums_excerpt.csv"), str(data_path / "raw_tracks_excerpt.csv"))
    tracks = track_reader.read_tracks_file()
    for row in tracks:
        id = int(row["track_id"])
        title = row['track_title']

        new_track = Track(int(row["track_id"]), row['track_title'])
        new_track.track_duration = int(float(row['track_duration']))
        new_track.track_url = row['track_url']
        new_track.set_song_url(row['track_file'])
        try:
            album_id = int(row['album_id'])
        except ValueError:
            album_id = 9999

        try:
            artist_id = int(row['artist_id'])
        except ValueError:
            artist_id = 9999
        #print(f"\n\n\n\n\n\n\n{new_track}\n\n\n\n\n\n\n\n\n")
        new_album = Album(album_id, row['album_title'])
        #print(f"\n\n\n\n\n\n\n{new_album}\n\n\n\n\n\n\n\n\n")
        new_artist = Artist(artist_id, row['artist_name'])
        #print(f"\n\n\n\n\n\n\n{new_artist}\n\n\n\n\n\n\n\n\n")

        new_track.album = new_album
        new_track.artist = new_artist

        genres = row["track_genres"]
        if len(genres) > 0:
            genres = ast.literal_eval(genres)
            # print("Test5")
            for genre in genres:
                genre_id = int(genre["genre_id"])
                genre_title = genre["genre_title"]
                genre = Genre(genre_id, genre_title)
                new_track.add_genre(genre)
                repo.add_genre(genre, new_track)
        repo.add_album(new_album, new_track)
        repo.add_artist(new_artist, new_track)
        repo.add_track(new_track)



