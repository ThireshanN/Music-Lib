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
