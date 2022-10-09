from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.exc import NoResultFound
# from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.adapters.repository import AbstractRepository
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.track import Track
from music.domainmodel.user import User
from music.domainmodel.review import Review
from bisect import bisect, bisect_left, insort_left


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
        self.__artist_index = dict()
        self.__album_index = dict()
        self.__genre_index = dict()
        self.__artist_to_track_dic = dict()
        self.__album_to_track_dic = dict()
        self.__genre_to_track_dic = dict()

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def get_user_id(self, userid) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_id == userid).one()
        except NoResultFound:
            pass
        return user

    def get_playlist_tracks(self):  # To Do - Need to implement playlist
        pass
        # return self.__playlist.get_all_tracks()

    def delete_from_playlist(self, track):  # To Do
        pass
        # self.__playlist.remove_track(track)

    def add_to_playlist(self, track):  # To Do
        pass
        # self.__playlist.add_track(track)

<<<<<<< Updated upstream
    def get_review(self):  # To Do
        pass
        # return self.__track_to_review

    def post_review(self, review):  # To Do
        pass
        # k = review.track.track_id
        # if k in self.__track_to_review:
        #    self.__track_to_review[k].append(review)
        # else:
        #    self.__track_to_review[k] = [review]
=======
    def get_review(self):
        pass
        print("Get Review 1")
        operators = self._session_cm.session.query(Review).all()
        print("Get Review 2")
        #operators = [op.login for op in operators]
        track_to_review_dict = dict()
        print("Get Review 3")
        for review in operators:
            print("Get Review 4")
            k = review.track_id
            print("Get Review 5")
            if k in track_to_review_dict:
                print("Get Review 6")
                track_to_review_dict[k].append(review)
                print("Get Review 7")
            else:
                track_to_review_dict[k] = [review]
        return track_to_review_dict


    def post_review(self, review):  #To Do
        #super().post_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()
        print("post done")
>>>>>>> Stashed changes

    def get_all_users(self):
        return self._session_cm.session.query(User).all()

    def get_genre_collective(self, genre_id):
        return self.__genre_index, self.__genre_to_track_dic

    def get_artist_collective(self, artist_id):
        return self.__artist_index, self.__artist_to_track_dic

    def get_album_collective(self, album_id):
        return self.__album_index, self.__album_to_track_dic

    def add_genre(self, genre: Genre, track: Track):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()
        if genre.genre_id in self.__genre_to_track_dic:
            self.__genre_to_track_dic[genre.genre_id].append(track)
        else:
            self.__genre_to_track_dic[genre.genre_id] = [track]
        self.__genre_index[genre.genre_id] = genre

    def add_artist(self, artist: Artist, track: Track):
        with self._session_cm as scm:
            scm.session.merge(artist)
            scm.commit()
        if artist.artist_id in self.__artist_to_track_dic:
            self.__artist_to_track_dic[artist.artist_id].append(track)
        else:
            self.__artist_to_track_dic[artist.artist_id] = [track]
        self.__artist_index[artist.artist_id] = artist

    def add_album(self, album: Album, track: Track):
        with self._session_cm as scm:
            scm.session.merge(album)
            scm.commit()
        if album.album_id in self.__album_to_track_dic:
            self.__album_to_track_dic[album.album_id].append(track)
        else:
            self.__album_to_track_dic[album.album_id] = [track]
        self.__album_index[album.album_id] = album

    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.merge(track)
            scm.commit()

    def get_track(self, id: int) -> Track:
        track = None
        try:
            track = self._session_cm.session.query(Track).filter(Track._Track__track_id == id).one()
        except NoResultFound:
            pass
        return track

    def get_all_tracks(self) -> List[Track]:
        return self._session_cm.session.query(Track).all()

    def amount_of_tracks(self):
        return self._session_cm.session.query(Track).count()

    def get_first_track(self):
        track = self._session_cm.session.query(Track).first()
        return track

    def get_last_track(self):
        track = self._session_cm.session.query(Track).order_by(desc(Track._Track__track__id)).first()
        return track

    def get_previous_track(self, track: Track):  # Don't need
        pass

    def get_next_track(self, track: Track):  # Don't need
        pass

    def track_index(self, track: Track):  # To Do
        pass
        # index = bisect_left(self.__tracks, track)
        # if index != len(self.__tracks) and self.__tracks[index].track_id == track.track_id:
        #    return index
        # raise ValueError("in track index - mem repo")
