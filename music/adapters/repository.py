import abc
from typing import List

from music.domainmodel.track import Track

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
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
    def get_tracks_by_ids(self, random_ids):
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















