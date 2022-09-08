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
    def amount_of_tracks(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_by_id(self, id):
        raise NotImplementedError








