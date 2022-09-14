import csv
from abc import ABC
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.track import Track
from music.adapters.csvdatareader import create_track_object, TrackCSVReader


class MemoryRepository(AbstractRepository):
    # Tracks order by track_id,
    def __init__(self):
        self.__tracks: List[Track] = []
        self.__track_index = dict()

    def add_track(self, track: Track):
        self.__tracks.append(track)
        self.__track_index[track.track_id] = track

    def get_track(self, track_id: int) -> Track:
        track = None

        try:
            track = self.__track_index[track_id]
        except KeyError:
            pass

        return track

    def get_all_tracks(self) -> List[Track]:
        return self.__tracks

    def get_tracks_by_ids(self, id_list):
        existing_ids = [id for id in id_list if id in self.__track_index]
        tracks = [self.__track_index[id] for id in existing_ids]
        return tracks

    def amount_of_tracks(self):
        return len(self.__tracks)

    def get_first_tracks(self):
        tracks = None
        if len(self.__tracks) > 0:
            return self.__tracks[0]
        return tracks

    def get_last_tracks(self):
        tracks = None

        if len(self.__tracks) > 0:
            tracks = self.__tracks[-1]
        return tracks

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self.__tracks):
            raise StopIteration
        else:
            self._current += 1
            return self.__tracks[self._current - 1]

    def get(self, reference: int):
        return next((p for p in self.__tracks if p.track_id == reference), None)


def load_tracks(data_path: Path, repo: MemoryRepository):
    track_reader = TrackCSVReader(str(data_path / "raw_albums_excerpt.csv"), str(data_path / "raw_tracks_excerpt.csv"))
    tracks1 = track_reader.read_tracks_file()
    # tracks is type list
    for row in tracks1:
        id = int(row["track_id"])
        title = row['track_title']

        new_track = Track(int(row["track_id"]), row['track_title'])
        new_track.track_duration = int(float(row['track_duration']))
        new_track.track_url = row['track_url']
        try:
            album_id = int(row['album_id'])
        except ValueError:
            album_id = 9999

        try:
            artist_id = int(row['artist_id'])
        except ValueError:
            artist_id = 9999

        new_album = Album(album_id, row['album_title'])
        new_artist = Artist(artist_id, row['artist_name'])

        new_track.album = new_album
        new_track.artist = new_artist

        repo.add_track(new_track)


def populate(data_path: Path, repo: MemoryRepository):
    # Load tracks into the repository.
    load_tracks(data_path, repo)
