from flask import Blueprint, redirect, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, StringField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length


from bisect import bisect, bisect_left

from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from music.authentication.authentication import login_required

import music.adapters.repository as repo
from music.domainmodel.track import Track
from music.tracks import services

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

'''
@tracks_blueprint.route('/filtered')
def person_view():
    id = request.args.get('id', None)
    type = request.args.get('type', None)
    for person in people_repo:
        if person.id == person_id:
            # Task 5: Render the `people_view.html` template. It takes `img_url`,
            # 'firstname' and 'lastname' as variables.
            return render_template(
                'people_view.html',
                img_url=person.url,
                firstname=person.firstname,
                lastname=person.lastname,
            )
    return render_template('404.html')
'''


def track_index_subclass(track1: Track, track_list):
    index1 = bisect_left(track_list, track1)
    if index1 != len(track_list) and track_list[index1].track_id == track1.track_id:
        return index1
    raise ValueError("in track index - mem repo")


@tracks_blueprint.route('/filtered')
def person_view():
    id1 = request.args.get('person_id', 0)
    type1 = request.args.get('type', None)
    #print(id)
    #type = request.args.get('type', None)
    type1_obj = None
    tracks = None
    name = None
    if type1 == 'Artist':
        type1_obj, tracks = services.get_artists(id1, repo.repo_instance)
        if type1_obj is not None:
            name = type1_obj.full_name
    if type1 == 'Album':
        type1_obj, tracks = services.get_albums(id1, repo.repo_instance)
        if type1_obj is not None:
            name = type1_obj.title
    if type1 == 'Genre':
        type1_obj, tracks = services.get_genre(id1, repo.repo_instance)
        if type1_obj is not None:
            name = type1_obj.name

    #print(artist)
    if type1_obj is None or tracks is None or type1 is None:
        return render_template('404.html')
    print("test2")
    print(len(tracks))
    track = tracks[0]

    tracks_per_page = 10
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    next_tracks_url = None
    prev_tracks_url = None

    prev_track = next_track = None
    if len(tracks) > 0:
        try:
            index = track_index_subclass(track, tracks)
            for stored_track in reversed(tracks[0:index]):
                if stored_track.track_id < track.track_id:
                    prev_track = stored_track.track_id
                    break
        except ValueError:
            print("mem repo get prev track")
            pass

        try:
            index = track_index_subclass(track, tracks)
            for stored_track in tracks[index + 1:len(tracks)]:
                if stored_track.track_id > track.track_id:
                    next_track = stored_track.track_id
                    break
        except ValueError:
            print("mem repo get next track")
            pass
    print(len(tracks))
    curr_iter_tracks = tracks[cursor:cursor + tracks_per_page]

    if cursor > 0:
        prev_tracks_url = url_for('tracks_bp.person_view', cursor=cursor - tracks_per_page, person_id=id1, type=type1)
    if cursor + tracks_per_page < len(tracks):
        next_tracks_url = url_for('tracks_bp.person_view', cursor=cursor + tracks_per_page, person_id=id1, type=type1)

    print(prev_tracks_url)
    print(next_tracks_url)
    print(len(tracks))
    return render_template(
        'tracks/track_view.html',
        #title=track.title,
        #track_id=track.track_id,
        type=type1,
        id=id1,
        name_type=name,
        tracks=curr_iter_tracks,
        prev_tracks_url=prev_tracks_url,
        next_tracks_url=next_tracks_url,
    )






@tracks_blueprint.route('/find', methods=['GET', 'POST'])
def find_person():
    form = SearchForm()

    if form.validate_on_submit():
        print('test1')
        print(form.id.data)
        print(form.type.data)
        # TODO: Read id from the form and redirect to `people_blueprint.person_view`
        return redirect(
            url_for('tracks_bp.person_view', person_id=form.id.data, type=form.type.data)
        )
    else:
        # TODO: Render the `people_search.html` template. It takes `form` and
        # `handler_url` as parameters.
        return render_template(
            'tracks/track_search.html',
            form=form,
            handler_url=url_for('tracks_bp.find_person')
        )


class SearchForm(FlaskForm):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Genre', 'Genre')]
    type = SelectField('Search by:', choices=choices)
    id = IntegerField("Enter ArtistID/AlbumID/GenreID", [DataRequired()])
    submit = SubmitField("Search")



'''
class SearchForm(FlaskForm):
    # Task 6: Define the variables below using IntegerField and SubmitField
    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Genre', 'Genre')]
    select = SelectField('Search for music:', choices=choices)
    id = IntegerField("Id No. of Artist, Genre, or Album", [DataRequired()])
    submit = SubmitField("Search")
'''
'''

class SearchForm(FlaskForm):
    # Task 6: Define the variables below using IntegerField and SubmitField
    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Genre', 'Genre')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')

'''


@tracks_blueprint.route('/favourites')
@login_required
def playlist():
    add_track_id = request.args.get('add')
    delete_track_id = request.args.get('del')

    if add_track_id is not None:
        track = services.get_track_by_id(int(add_track_id), repo.repo_instance)
        #print(track.song_url)
        services.add_to_playlist(track, repo.repo_instance)

    if delete_track_id is not None:
        track = services.get_track_by_id(int(delete_track_id), repo.repo_instance)
        services.delete_from_playlist(track, repo.repo_instance)

    tracks = services.get_playlist_tracks(repo.repo_instance)

    if len(tracks) <= 0:
        curr_iter_tracks = None
        prev_tracks_url = None
        next_tracks_url = None
    else:
        track = tracks[0]

        tracks_per_page = 1
        cursor = request.args.get('cursor')

        if cursor is None:
            cursor = 0
        else:
            cursor = int(cursor)

        next_tracks_url = None
        prev_tracks_url = None

        prev_track = next_track = None
        if len(tracks) > 0:
            try:
                index = track_index_subclass(track, tracks)
                for stored_track in reversed(tracks[0:index]):
                    if stored_track.track_id < track.track_id:
                        prev_track = stored_track.track_id
                        break
            except ValueError:
                print("mem repo get prev track")
                pass

            try:
                index = track_index_subclass(track, tracks)
                for stored_track in tracks[index + 1:len(tracks)]:
                    if stored_track.track_id > track.track_id:
                        next_track = stored_track.track_id
                        break
            except ValueError:
                print("mem repo get next track")
                pass
        print(len(tracks))
        curr_iter_tracks = tracks[cursor:cursor + tracks_per_page]

        if cursor > 0:
            prev_tracks_url = url_for('tracks_bp.playlist', cursor=cursor - tracks_per_page)
        if cursor + tracks_per_page < len(tracks):
            next_tracks_url = url_for('tracks_bp.playlist', cursor=cursor + tracks_per_page)
    #print(curr_iter_tracks)
    return render_template(
        'playlist.html',
        tracks=curr_iter_tracks,
        prev_tracks_url = prev_tracks_url,
        next_tracks_url=next_tracks_url
    )
