from flask import Blueprint, request, url_for, render_template

from music.tracks import services
import music.adapters.repository as repo

# Configure Blueprint.
tracks_blueprint = Blueprint(
    'tracks_bp', __name__)


@tracks_blueprint.route('/tracks', methods=["GET"])
def list_tracks():
    tracks_per_page = 10
    id = request.args.get('id')
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    if id is None:
        # No id query parameter, so initialise id to start at the beginning.
        id = 2
    else:
        # Convert id from string to int.
        id = int(id)

    first_tracks_url = None
    last_tracks_url = None
    next_tracks_url = None
    prev_tracks_url = None

    tracks = services.get_all_tracks(repo.repo_instance)  # gets all tracks in the repo
    tracks = tracks[cursor:cursor+tracks_per_page]  # slices the tracks based on tracks_per_page

    if cursor > 0:
        #prev_tracks_url = url_for('tracks_bp.tracks', cursor=cursor-tracks_per_page)
        first_tracks_url = url_for('tracks_bp.tracks')

    if cursor + tracks_per_page < len(tracks):
        next_tracks_url = url_for('tracks_bp.tracks',  cursor=cursor + tracks_per_page)

        last_cursor = tracks_per_page * int(len(tracks) / tracks_per_page)
        if len(tracks) % tracks_per_page == 0:
            last_cursor -= tracks_per_page
        last_tracks_url = url_for('tracks_bp.tracks', cursor=last_cursor)

    # Generate the webpage to display the articles.
    return render_template(
        'tracks/track_list.html',
        tracks=tracks,
        prev_tracks_url=prev_tracks_url,
        next_tracks_url=next_tracks_url,
        last_tracks_url=last_tracks_url,
        first_tracks_url=first_tracks_url
    )