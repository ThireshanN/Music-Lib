import random as rand

from werkzeug.security import generate_password_hash, check_password_hash

from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass

def get_all_users(repo: AbstractRepository):
    all_users = repo.get_all_users()
    return all_users


def add_user(user_name: str, password: str, repo: AbstractRepository):
    # Check that the given user name is available.
    #print(user_name)
    #print((password))
    user_id = rand.randrange(1, 1000000000)
    user = repo.get_user(user_name)
    user_from_id = repo.get_user_id(user_id)
    if user is not None:
        raise NameNotUniqueException
    while user_from_id is not None:
        user_id = rand.randrange(1, 1000000000)
        user_from_id = repo.get_user_id(user_id)

    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)

    #print(user_name)
    #print((password))
    #print(user_id)
    # Create and store the new User, with password encrypted.
    user = User(user_id =user_id, user_name=user_name, password=password_hash)
    #print(user.user_id)
    #print(user.user_name)
    #print(password_hash)
    repo.add_user(user)


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


# ===================================================
# Functions to convert model entities to dictionaries
# ===================================================

def user_to_dict(user: User):
    user_dict = {
        'user_name': user.user_name,
        'password': user.password,
        'user_id' : user.user_id
    }
    return user_dict
