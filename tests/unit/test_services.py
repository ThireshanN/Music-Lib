import pytest

from music.authentication.services import AuthenticationException
from music.authentication import services as auth_services
from music.comments.services import NonExistentTrackException


def test_can_add_user(in_memory_repo):
    new_user_name = "tom"
    new_password = "Tomfretwell@30"

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo): #user not being added
    user_name = 'tom'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)