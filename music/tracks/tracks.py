from flask import Blueprint, request, url_for, render_template
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

from music.domainmodel.track import Track
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


@tracks_blueprint.route("/track/<int:track_id>")
def track_view(track_id):
    track = services.get_track_by_id(track_id, repo.repo_instance)
    if track is None:
        return render_template("404.html")

    return render_template(
        "tracks/track_view.html",
        track_id=track.track_id,
        track_title=track.title,
        album_name=track.album.title,
        artist_name=track.artist.full_name,
        track_duration=track.track_duration,
        track_url=track.track_url
    )


@tracks_blueprint.route("/find", methods=["GET", "POST"])
def find_albums():
    form = SearchForm()
    if form.validate_on_submit():
        print(f"Here is the data being passed from the search field {form.id.data}")
        return redirect(url_for("tracks_bp.track_view", track_id=form.id.data))

    else:
        return render_template(
            "tracks/track_search.html",
            form=form,
            handler_url=url_for("tracks_bp.find_albums"))


class SearchForm(FlaskForm):
    # Task 6: Define the variables below using IntegerField and SubmitField
    id = IntegerField("Enter Album Title", [DataRequired()])
    submit = SubmitField("Search")
