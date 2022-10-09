import abc
from typing import List

from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.track import Track
from music.domainmodel.user import User

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_to_playlist(self, track):
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlist_tracks(self):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_from_playlist(self, track):
        raise NotImplementedError

    @abc.abstractmethod
    def post_review(self, review):
        raise NotImplementedError

    @abc.abstractmethod
    def get_review(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_artist_collective(self, artist_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_album_collective(self, album_id):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre_collective(self, genre_id):
        raise NotImplementedError

    @abc.abstractmethod
    def add_album(self, album: Album, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, artist: Artist, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_users(self) -> List[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_id(self, userid) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, track_id) -> Track:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_tracks(self) -> List[Track]:
        raise NotImplementedError

    @abc.abstractmethod
    def amount_of_tracks(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_previous_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def track_index(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_track(self) -> Track:
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_track(self) -> Track:
        raise NotImplementedError
