import pytest

from music.authentication.services import AuthenticationException, NameNotUniqueException
from music.authentication import services as auth_services
from music.tracks.services import NonExistentTrackException
from music.tracks import services as track_services
from music.comments.services import NonExistentTrackException
from music.comments import services as comment_services


def test_can_add_user(in_memory_repo):
    new_user_name = "jz"
    new_password = "abcd1A23"

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):  # user not being added
    user_name = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)

    try:
        auth_services.add_user(user_name, password, in_memory_repo)
    except NameNotUniqueException:
        assert True



def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)


def test_get_first_track(in_memory_repo):
    track_as_dict = track_services.get_first_track(in_memory_repo)
    assert track_as_dict['id'] == 2


def test_get_last_track(in_memory_repo):
    track_as_dict = track_services.get_last_track(in_memory_repo)
    assert track_as_dict['id'] == 3661


def test_get_all_tracks_prev_next_id(in_memory_repo):
    tracks = track_services.get_all_tracks(in_memory_repo)
    assert len(tracks) == 3


def test_get_album_by_id(in_memory_repo):
    albums = track_services.get_albums(1, in_memory_repo)
    assert len(albums) == 2


def test_get_artist_by_id(in_memory_repo):
    artists = track_services.get_artists(1, in_memory_repo)
    assert len(artists) == 2


def test_get_genre_by_id(in_memory_repo):
    genres = track_services.get_genre(1, in_memory_repo)
    assert len(genres) == 2


def test_get_non_exist_track_in_comment(in_memory_repo):
    with pytest.raises(NonExistentTrackException):
        comments_as_dict = comment_services.get_track_by_id(1, in_memory_repo)


def test_add_comment(in_memory_repo):
    track_id = 2
    comment = "Adding new comment"
    rating = 1
    comment_services.add_comment(track_id, comment, rating, in_memory_repo)
    assert len(comment_services.get_reviews(in_memory_repo)) == 1


def test_get_records(in_memory_repo):
    track_id = 2
    comment = "Adding new comment"
    rating = 1
    comment_services.add_comment(track_id, comment, rating, in_memory_repo)
    track_id = 3
    comment = "Adding new comment1"
    rating = 2
    comment_services.add_comment(track_id, comment, rating, in_memory_repo)

    assert len(comment_services.get_reviews(in_memory_repo)) == 2