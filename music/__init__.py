"""Initialize Flask app."""

import os
from pathlib import Path

from flask import Flask
from flask_wtf.csrf import CSRFProtect

import music.adapters.repository as repo
from music.adapters.memory_repository import MemoryRepository, populate


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    csrf = CSRFProtect()
    csrf.init_app(app)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('music') / 'adapters' / 'data'

<<<<<<< HEAD
    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill the content of the repository from the provided csv files
    populate(data_path, repo.repo_instance)

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from music.blueprints.track_blueprint import track_blueprint
        app.register_blueprint(track_blueprint)

    return app
=======
#Testing first commit - In Repo without the github
>>>>>>> d213905ea60aeb400a998b08ddb6df6c73724aa5
