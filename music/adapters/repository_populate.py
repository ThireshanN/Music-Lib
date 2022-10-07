from pathlib import Path

from music import MemoryRepository
from music.adapters.csv_data_importer import load_tracks
from music.adapters.repository import AbstractRepository


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    load_tracks(data_path, repo, database_mode)

