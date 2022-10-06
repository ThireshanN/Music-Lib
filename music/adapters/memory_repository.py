import ast
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
from music.domainmodel.user import User
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.adapters.csvdatareader import create_track_object, TrackCSVReader


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__tracks: List[Track] = []
        self.__track_index = dict()
        self.__artist_index = dict()
        self.__album_index = dict()
        self.__genre_index = dict()
        self.__users = []
        self.__artist_to_track_dic = dict()
        self.__album_to_track_dic = dict()
        self.__genre_to_track_dic = dict()
        self.__track_to_review = dict()
        self.__playlist = PlayList()

    def get_playlist_tracks(self):
        return self.__playlist.get_all_tracks()

    def delete_from_playlist(self, track):
        self.__playlist.remove_track(track)

    def add_to_playlist(self, track):
        self.__playlist.add_track(track)

    def get_review(self):
        return self.__track_to_review

    def post_review(self, review):
        k = review.track.track_id
        if k in self.__track_to_review:
            self.__track_to_review[k].append(review)
        else:
            self.__track_to_review[k] = [review]

    def get_all_users(self):
        return self.__users

    def get_genre_collective(self):
        return self.__genre_index, self.__genre_to_track_dic

    def get_artist_collective(self):
        return self.__artist_index, self.__artist_to_track_dic

    def get_album_collective(self):
        return self.__album_index, self.__album_to_track_dic

    def add_genre(self, genre: Genre, track: Track):
        if genre.genre_id in self.__genre_to_track_dic:
            self.__genre_to_track_dic[genre.genre_id].append(track)
        else:
            self.__genre_to_track_dic[genre.genre_id] = [track]
        self.__genre_index[genre.genre_id] = genre

    def add_artist(self, artist: Artist, track: Track):
        if artist.artist_id in self.__artist_to_track_dic:
            self.__artist_to_track_dic[artist.artist_id].append(track)
        else:
            self.__artist_to_track_dic[artist.artist_id] = [track]
        self.__artist_index[artist.artist_id] = artist

    def add_album(self, album: Album, track: Track):
        if album.album_id in self.__album_to_track_dic:
            self.__album_to_track_dic[album.album_id].append(track)
        else:
            self.__album_to_track_dic[album.album_id] = [track]
        self.__album_index[album.album_id] = album

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user_id(self, userid) -> User:
        return next((user for user in self.__users if user.user_id == userid), None)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

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

    def get_first_track(self):
        track = None

        if len(self.__tracks) > 0:
            track = self.__tracks[0]
        return track

    def get_last_track(self):
        track = None

        if len(self.__tracks) > 0:
            track = self.__tracks[-1]

        return track

    def get_previous_track(self, track: Track):
        prev_track = None
        try:
            index = self.track_index(track)
            for stored_track in reversed(self.__tracks[0:index]):
                if stored_track.track_id < track.track_id:
                    prev_track = stored_track.track_id
                    break
        except ValueError:
            print("mem repo get prev track")
            pass

        return prev_track

    def get_next_track(self, track: Track):
        next_track = None
        try:
            index = self.track_index(track)
            for stored_track in self.__tracks[index + 1:len(self.__tracks)]:
                if stored_track.track_id > track.track_id:
                    next_track = stored_track.track_id
                    break
        except ValueError:
            pass

        return next_track

    def track_index(self, track: Track):
        index = bisect_left(self.__tracks, track)
        if index != len(self.__tracks) and self.__tracks[index].track_id == track.track_id:
            return index
        raise ValueError("in track index - mem repo")

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


def load_tracks(data_path: Path, repo: AbstractRepository, database_mode: bool):
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

        new_album = Album(album_id, row['album_title'])
        new_artist = Artist(artist_id, row['artist_name'])

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


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    load_tracks(data_path, repo, database_mode)
