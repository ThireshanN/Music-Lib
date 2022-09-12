from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

from music.adapters.repository import repo_instance
from music.domainmodel.track import Track

track_blueprint = Blueprint('track_blueprint', __name__)


@track_blueprint.route('/')
def home():
    # Task 3: Render our home page.
    return render_template('home.html')


@track_blueprint.route('/tracks')
def list_tracks():
    return render_template('track_list.html', tracks_class=repo_instance)


@track_blueprint.route('/find', methods=['GET', 'POST'])
def find_track():
    # Task 7: Complete this method
    form = SearchForm()

    # `handler_url` as parameters.
    return render_template(
        'track_search.html',
        form=form,
        handler_url=url_for('track_blueprint.find_track')
    )


class SearchForm(FlaskForm):
    # Task 6: Define the variables below using IntegerField and SubmitField
    id = IntegerField("Enter Track ID", [DataRequired()])
    submit = SubmitField("Search")
