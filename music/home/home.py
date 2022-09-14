from flask import Blueprint, render_template

import music.utilities.utilities as utilities


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/')
def home():
    # Task 3: Render our home page.
    return render_template('home/home.html')