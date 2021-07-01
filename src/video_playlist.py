"""A video playlist class."""
from typing import Sequence

class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, playlist_title: str, playlist_id: str, playlist_videos):
        self._title = playlist_title
        self._playlist_id = playlist_id
        self._videos = list(playlist_videos)
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def playlist_id(self) -> str:
        return self._playlist_id
    
    @property
    def videos(self) -> Sequence[str]:
        return self._videos
