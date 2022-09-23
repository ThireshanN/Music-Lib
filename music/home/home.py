from flask import Blueprint, render_template

import music.utilities.utilities as utilities


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/')
def home():
    return render_template('home/home.html')