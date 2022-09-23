from typing import Iterable
import random

from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track


def get_random_tracks(quantity, repo: AbstractRepository):
    track_count = repo.amount_of_tracks()

    if quantity >= track_count:
        quantity = track_count - 1

    random_ids = random.sample(range(1, track_count), quantity)
    tracks = repo.get_tracks_by_ids(random_ids)

    return tracks_to_dict(tracks)


# ============================================
# Functions to convert dicts to model entities
# ============================================
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


def tracks_to_dict(tracks: Iterable[Track]):
    return [track_to_dict(track) for track in tracks]
