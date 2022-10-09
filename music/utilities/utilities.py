from bisect import bisect_left

from flask import Blueprint, url_for

from music.utilities import services
import music.adapters.repository as repo

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_selected_tracks(quantity=15):
    tracks = services.get_random_tracks(quantity, repo.repo_instance)

    for track in tracks:
        track['hyperlink'] = url_for('news_bp.articles_by_date', id=track['track_id'].isoformat())
    return tracks


def track_index_subclass(track1, track_list):
    print('testA')
    index1 = bisect_left(track_list, track1)
    print('testB')
    if index1 != len(track_list) and track_list[index1] == track1:
        print('testC')
        return index1
    print('testD')
    raise ValueError("in track index - mem repo")
