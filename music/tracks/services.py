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


def get_last_track(repo: AbstractRepository):
    tracks = repo.get_last_track()
    return track_to_dict(tracks)


def get_first_track(repo: AbstractRepository):
    track = repo.get_first_track()
    return track_to_dict(track)


def get_tracks(repo: AbstractRepository):
    tracks = repo.get_all_tracks()  # returns all tracks
    track_dto = list()
    prev_id = next_id = None
    if len(tracks) > 0:
        prev_id = repo.get_previous_track(tracks[0])
        next_id = repo.get_next_track(tracks[0])
        track_dto = tracks_to_dict(tracks)

    return track_dto, prev_id, next_id


def track_to_dict(track: Track):
    track_dict = {
        'id': track.track_id,
        'title': track.title,
        'album_title': track.album.title,
        'artist_fullname': track.artist.full_name,
        'track_duration': track.track_duration,
        'track_url': track.track_url
    }
    return track_dict


def get_all_tracks(repo: AbstractRepository):
    all_tracks = repo.get_all_tracks()
    prev_tracks = next_track = None
    if len(all_tracks) > 0:
        prev_tracks = repo.get_previous_track(all_tracks[0])
        next_track = repo.get_next_track(all_tracks[0])

    return all_tracks, prev_tracks, next_track
    # return repo.get_all_tracks()


def tracks_to_dict(tracks: Iterable[Track]):
    return [track_to_dict(track) for track in tracks]


def get_albums(album_id, repo: AbstractRepository):
    album_id = int(album_id)
    albums_index_dict, albums_to_tracks = repo.get_album_collective()
    if album_id not in albums_index_dict:
        return None, None
    album = albums_index_dict[album_id]
    list_of_tracks = albums_to_tracks[album_id]
    return album, list_of_tracks


def get_artists(artist_id, repo: AbstractRepository):
    artist_id = int(artist_id)
    artist_index_dict, artist_to_tracks = repo.get_artist_collective()
    if artist_id not in artist_index_dict:
        return None, None
    artist = artist_index_dict[artist_id]
    list_of_tracks = artist_to_tracks[artist_id]
    return artist, list_of_tracks


def get_genre(genre_id, repo: AbstractRepository):
    genre_id = int(genre_id)
    genre_index_dict, genre_to_tracks = repo.get_genre_collective()
    if genre_id not in genre_index_dict:
        return None, None
    genre = genre_index_dict[genre_id]
    list_of_tracks = genre_to_tracks[genre_id]
    return genre, list_of_tracks
