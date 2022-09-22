from typing import List

import pytest

from music.adapters.repository import RepositoryException
from music.domainmodel.track import Track


def test_repository_can_get_track(in_memory_repo):
    track = in_memory_repo.get_track(2)
    print(f"\nHere is what is being returned 1 = {track}")
    assert track == Track(2, "Food")

# Check Piazza for response on how to write this correctly.


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
    #Can't figure out how to get the title of the track
    #not sure why i can't


def test_repository_get_track_amount(in_memory_repo):
    tracks = in_memory_repo.amount_of_tracks()
<<<<<<< HEAD
    assert tracks == 2000
=======
    assert tracks == 2000
>>>>>>> feature_update
