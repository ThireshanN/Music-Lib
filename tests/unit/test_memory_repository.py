from typing import List

import pytest

from music.adapters.repository import RepositoryException
from music.domainmodel.genre import Genre
from music.domainmodel.track import Track
from music.domainmodel.user import User


def test_repository_can_get_track(in_memory_repo):
    track = in_memory_repo.get_track(2)
    assert track == Track(2, "Food")


def test_repository_does_not_retrieve_track(in_memory_repo):
    track = in_memory_repo.get_track(99999)
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


def test_get_next_track(in_memory_repo):
    track = in_memory_repo.get_track(2)
    next_track = in_memory_repo.get_next_track(track)
    expected_track = in_memory_repo.get_track(3)
    assert next_track == expected_track.track_id


def test_get_prev_track(in_memory_repo):
    track = in_memory_repo.get_track(3)
    prev_track = in_memory_repo.get_previous_track(track)
    expected_track = in_memory_repo.get_track(2)
    assert prev_track == expected_track.track_id


def test_get_user_by_username(in_memory_repo):
    user = User(1, "tester", "password")
    in_memory_repo.add_user(user)
    test_user = in_memory_repo.get_user("tester")

    assert user == test_user


def test_get_user_by_invalid_username(in_memory_repo):
    user = User(1, "tester", "password")
    in_memory_repo.add_user(user)
    test_user = in_memory_repo.get_user("incorrect")

    assert test_user is None
