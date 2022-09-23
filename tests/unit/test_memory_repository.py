from typing import List

import pytest

from music.adapters.repository import RepositoryException
from music.domainmodel.genre import Genre
from music.domainmodel.track import Track


def test_repository_can_get_track(in_memory_repo):
    track = in_memory_repo.get_track(2)
    print(f"\nHere is what is being returned 1 = {track}")
    assert track == Track(2, "Food")


def test_repository_does_not_retrieve_track(in_memory_repo):
    track = in_memory_repo.get_track(99999)
    print(f"\nHere is what is being returned 2 = {track}")
    assert track is None


def test_repository_get_all_tracks(in_memory_repo):
    tracks = in_memory_repo.get_all_tracks()
    assert len(tracks) != 0


def test_repository_get_next_track(in_memory_repo):
    track = in_memory_repo.get_track(2)
    next_track = in_memory_repo.get_next_track(track)
    # Can't figure out how to get the title of the track
    # not sure why i can't


def test_repository_get_track_amount(in_memory_repo):
    tracks = in_memory_repo.amount_of_tracks()
    assert tracks == 2000


def test_add_genre_with_track_attached(in_memory_repo):  # There no way for me to test this as everything in tuples
    track = in_memory_repo.get_track(2)
    genre = Genre(9999, "tester")
    in_memory_repo.add_genre(genre, track)
    new_genre = in_memory_repo.get_genre_collective()[genre]

    # genres_count = len(in_memory_repo.get_genre_collective())
    assert new_genre is not None


def test_add_genre_without_track_attached(in_memory_repo):
    genre = Genre(9999, "tester")
    with pytest.raises(RepositoryException):
        in_memory_repo.add_genre(genre, None)
