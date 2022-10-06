from pathlib import Path

from music import MemoryRepository
from music.adapters.memory_repository import load_tracks
from music.adapters.repository import AbstractRepository


def populate(data_path: Path, repo: MemoryRepository, database_mode: bool):
    load_tracks(data_path, repo, database_mode)