from datetime import date, datetime

import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.adapters.repository import RepositoryException
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.track import Track


def test_repository_can_get_track_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_all_tracks()

    assert len(tracks) == 2000


def test_repository_can_add_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = Track(123123123123, "tester")
    repo.add_track(track)

    assert repo.get_track(123123123123) == track


def test_repo_can_get_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(2)

    assert track.title == "Food"
    assert track.track_url == "http://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life/Food"
    assert track.track_duration == "168"
    assert track.song_url == "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/WFMU/AWOL/AWOL_-_A_Way_Of_Life/AWOL_-_03_-_Food.mp3"


def test_repo_does_not_retrieve_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(1)
    assert track is None


def test_repo_get_first_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    first_track = repo.get_first_track()
    assert first_track.track_id == 2
    assert first_track.title == "Food"


def test_get_the_last_track_entry(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    last_track = repo.get_last_track()
    assert last_track.track_id == 3661
    assert last_track.title == "yet to be titled"


def test_repo_can_get_artist_collective(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artists = repo.get_artist_collective(4)
    matching_artist = artists[0]
    track_to_artist = artists[1]

    assert len(matching_artist) == 1
    assert len(track_to_artist.keys()) == 1


def test_post_new_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_reviews = len(repo.get_review())
    track = repo.get_track(2)
    review = Review(track, "this is a test review", 5)
    repo.post_review(review)

    assert number_of_reviews + 1 == len(repo.get_review())


def test_get_empty_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    review = repo.get_review()

    assert len(review) == 0


def test_adding_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    length_before_add = repo.get_genre_length()
    genre = Genre(9999, "tester")
    repo.add_genre(genre, Track(191919191, "Testing"))

    assert repo.get_genre_length() == length_before_add + 1
