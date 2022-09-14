from flask import Blueprint, request, url_for, render_template

from music.tracks import services
import music.adapters.repository as repo

# Configure Blueprint.
tracks_blueprint = Blueprint(
    'tracks_bp', __name__)


@tracks_blueprint.route('/tracks', methods=["GET"])
def list_tracks():
    tracks_per_page = 13
    cursor = request.args.get('cursor')

    if cursor is None:

        cursor = 0
    else:

        cursor = int(cursor)

    first_tracks_url = None
    last_tracks_url = None
    next_tracks_url = None
    prev_tracks_url = None

    all_tracks, pre_track, next_track = services.get_all_tracks(repo.repo_instance)
    tracks = all_tracks[cursor:cursor + tracks_per_page]

    if cursor > 0:
        prev_tracks_url = url_for('tracks_bp.list_tracks', cursor=cursor - tracks_per_page)
        first_tracks_url = url_for('tracks_bp.list_tracks')
    if cursor + tracks_per_page < len(all_tracks):
        next_tracks_url = url_for('tracks_bp.list_tracks', cursor=cursor + tracks_per_page)

        last_cursor = tracks_per_page * int(len(all_tracks) / tracks_per_page)
        if len(all_tracks) % tracks_per_page == 0:
            last_cursor -= tracks_per_page
        last_tracks_url = url_for('tracks_bp.list_tracks', cursor=last_cursor)

    return render_template(
        'tracks/track_list.html',
        tracks=tracks,
        prev_tracks_url=prev_tracks_url,
        next_tracks_url=next_tracks_url,
        last_tracks_url=last_tracks_url,
        first_tracks_url=first_tracks_url
    )
