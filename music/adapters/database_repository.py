from typing import List

from sqlalchemy import desc, asc, delete, and_
from sqlalchemy.exc import NoResultFound
# from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import session

from music.adapters.repository import AbstractRepository
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
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
        self.__genre_index = dict()
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
        userid = int(session['user_id'])
        operators = self._session_cm.session.query(PlayList).filter(PlayList._PlayList__playlist_id == userid).all()
        ret_list = []
        track_id_list = []
        for ele in operators:
            k = ele.track_id
            if k not in track_id_list:
                track_id_list.append(k)
                ret_list.append(self.get_track(k))
            else:
                pass
        return ret_list

    def delete_from_playlist(self, track):  # To Do
        pass
        userid = int(session['user_id'])
        self._session_cm.session.query(PlayList).filter(
            and_(PlayList._PlayList__playlist_id == userid, PlayList._PlayList__track_id == track.track_id)).delete(
            synchronize_session=False)
        self._session_cm.commit()

    def add_to_playlist(self, track):  # To Do
        with self._session_cm as scm:
            temp = PlayList(int(session['user_id']))
            temp.track_id = track.track_id
            scm.session.add(temp)
            scm.commit()

    def get_review(self):
        operators = self._session_cm.session.query(Review).all()
        track_to_review_dict = dict()
        for review in operators:
            k = review.track_id
            if k in track_to_review_dict:
                track_to_review_dict[k].append(review)
            else:
                track_to_review_dict[k] = [review]
        return track_to_review_dict

    def post_review(self, review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_all_users(self):
        return self._session_cm.session.query(User).all()

    def get_genre_collective(self, genre_id):
        '''
        genre_index = dict()
        tracks = self._session_cm.session.query(Track).all()
        for element in tracks:
            genre_id = element.genres
            print(genre_id)
        return self.__genre_index, self.__genre_to_track_dic
        '''
        tracks = self._session_cm.session.execute('SELECT id, genre_string  FROM tracks').all()
        genre_table = self._session_cm.session.execute('SELECT * FROM genres').all()
        genre_to_track_dic = dict()
        genre_index = dict()
        for ele in tracks:
            track_id = int(ele[0])
            tk = self.get_track(track_id)
            listt = str(ele[1]).split(',')
            for ele2 in listt:
                try:
                    g_id = int(ele2)
                    if g_id in genre_to_track_dic:
                        genre_to_track_dic[g_id].append(tk)
                    else:
                        genre_to_track_dic[g_id] = [tk]
                except ValueError:
                    print("No Genres")
        for ele in genre_table:
            gen_id = int(ele[0])
            gen_name = str(ele[1])
            gen_to_add = Genre(gen_id, gen_name)
            genre_index[gen_id] = gen_to_add
        return genre_index, genre_to_track_dic


    def get_artist_collective(self, artist_id):
        artist_index = dict()
        artist_to_track_dict = dict()
        tracks = self._session_cm.session.execute('SELECT * FROM tracks WHERE artist_id = :artist_id', {'artist_id':
                                                                                                            artist_id}).all()
        artists = self._session_cm.session.execute('SELECT * FROM artists WHERE id = :artist_id', {'artist_id':
                                                                                                       artist_id}).all()
        artist_name = ""

        for element in artists:
            a_id = int(element[0])
            artist_name = str(element[1])
            artist = Artist(a_id, artist_name)
            if a_id in artist_index:
                artist_index[a_id].append(artist)
            else:
                artist_index[a_id] = artist

        for element in tracks:
            a_id = int(element[2])
            track_obj = Track(int(element[0]), str(element[1]))
            artist_obj = Artist(a_id, artist_name)
            alb_id = int(element[3])
            album_row = self._session_cm.session.execute('SELECT * FROM albums WHERE id = :album_id',
                                                         {'album_id': alb_id}).fetchone()
            album_obj = Album(int(album_row[0]), str(album_row[1]))
            track_obj.artist = artist_obj
            track_obj.album = album_obj
            if a_id in artist_to_track_dict:
                artist_to_track_dict[a_id].append(track_obj)
            else:
                artist_to_track_dict[a_id] = [track_obj]

        return artist_index, artist_to_track_dict

    def get_album_collective(self, album_id):
        album_index = dict()
        album_to_track_dict = dict()
        tracks = self._session_cm.session.execute('SELECT * FROM tracks WHERE album_id = :album_id', {'album_id':
                                                                                                          album_id}).all()
        albums = self._session_cm.session.execute('SELECT * FROM albums WHERE id = :album_id', {'album_id':
                                                                                                    album_id}).all()
        album_name = ""

        for element in albums:
            a_id = int(element[0])
            album_name = str(element[1])
            album = Album(a_id, album_name)
            if a_id in album_index:
                album_index[a_id].append(album)
            else:
                album_index[a_id] = album

        for element in tracks:
            a_id = int(element[3])
            track_obj = Track(int(element[0]), str(element[1]))
            album_obj = Album(a_id, album_name)
            art_id = int(element[2])
            artist_row = self._session_cm.session.execute('SELECT * FROM artists WHERE id = :album_id',
                                                          {'album_id': art_id}).fetchone()
            artist_obj = Artist(int(artist_row[0]), str(artist_row[1]))
            track_obj.artist = artist_obj
            track_obj.album = album_obj
            if a_id in album_to_track_dict:
                album_to_track_dict[a_id].append(track_obj)
            else:
                album_to_track_dict[a_id] = [track_obj]

        return album_index, album_to_track_dict

    def add_genre(self, genre: Genre, track: Track):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()


        # below is the same implementation as the mem_repo <- not persistent

        '''

        if genre.genre_id in self.__genre_to_track_dic:
            self.__genre_to_track_dic[genre.genre_id].append(track)
        else:
            self.__genre_to_track_dic[genre.genre_id] = [track]
        self.__genre_index[genre.genre_id] = genre
        '''

    def add_artist(self, artist: Artist, track: Track):
        with self._session_cm as scm:
            scm.session.merge(artist)
            scm.commit()

    def add_album(self, album: Album, track: Track):
        with self._session_cm as scm:
            scm.session.merge(album)
            scm.commit()

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
        track = self._session_cm.session.query(Track).order_by(desc(Track._Track__track_id)).first()
        return track

    def get_genre_length(self):
        genres = self._session_cm.session.query(Genre).all()
        return len(genres)

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
