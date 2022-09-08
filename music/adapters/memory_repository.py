import csv
from abc import ABC
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.track import Track
from music.adapters.csvdatareader import create_track_object, TrackCSVReader


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.
    def __init__(self, *args):
        self.__tracks: List[Track]= []
        self.__track_index = dict()
        for track in args:

            self.__tracks.append(track)
            self.__track_index[track.track_id] = track

    def add_track(self, track: Track):
        self.__tracks.append(track)
        self.__track_index[track.track_id] = track

    def get_track(self, track_id) -> Track:
        return next((track for track in self.__tracks if track.track_id == track_id), None)

    def amount_of_tracks(self):
        return len(self.__tracks)

    def get_track_by_id(self, id):
        try:
            return self.__track_index[id]
        except KeyError:
            return None

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

    def tracks_dict(self):
        return self.__track_index


def load_tracks(data_path: Path, repo: MemoryRepository):
    track_reader = TrackCSVReader(str(data_path / "raw_albums_excerpt.csv"), str(data_path / "raw_tracks_excerpt.csv"))
    tracks = track_reader.read_csv_files()
    #tracks is type list
    for row in tracks:
        repo.add_track(row)


def populate(data_path: Path, repo: MemoryRepository):
    # Load tracks into the repository.
    load_tracks(data_path, repo)

