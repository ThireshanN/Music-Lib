from typing import Iterable

from music.adapters.repository import AbstractRepository
from music.domainmodel.review import Review
from music.domainmodel.track import Track


class NonExistentTrackException(Exception):
    pass


def get_track_by_id(track_id: int, repo: AbstractRepository):
    track = repo.get_track(track_id)
    if track is None:
        raise NonExistentTrackException
    else:
        return track


def add_comment(track_id, comment, rating, repo: AbstractRepository):
    track = get_track_by_id(track_id, repo)
    review = Review(track, comment, rating)
    repo.post_review(review)


def get_reviews(repo: AbstractRepository):
    return repo.get_review()
