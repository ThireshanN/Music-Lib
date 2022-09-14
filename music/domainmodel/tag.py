from typing import Iterable, List

from music.domainmodel.track import Track


class Tag:
    def __init__(self, tag_name: str):
        self.__tag_name: str = tag_name
        self.__tagged_tracks: List[Track] = list()

    @property
    def tag_name(self) -> str:
        return self.__tag_name

    @property
    def tagged_articles(self) -> Iterable[Track]:
        return iter(self.__tagged_tracks)

    @property
    def number_of_tagged_articles(self) -> int:
        return len(self.__tagged_tracks)

    def is_applied_to(self, article: Track) -> bool:
        return article in self.__tagged_tracks

    def add_article(self, track: Track):
        self.__tagged_tracks.append(track)

    def __eq__(self, other):
        if not isinstance(other, Tag):
            return False
        return other.tag_name == self.tag_name