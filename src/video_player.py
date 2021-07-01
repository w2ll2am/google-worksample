"""A video player class."""

from os import X_OK
from src import video, video_playlist
from .video_library import VideoLibrary
from random import randint

from src import video_library

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_video = None
        self._paused_video = 0
        self._playlists = []
        self._all_videos = VideoLibrary().get_all_videos()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        rawVideos = self._video_library.get_all_videos()

        unsortedVideos = []
        for video in rawVideos:
            videoTags = " ".join(video.tags)
            unsortedVideos.append(f"{self._video_library.format(video)}")
        sortedVideos = sorted(unsortedVideos)
        [print(videoInformation) for videoInformation in sortedVideos]


    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        oldVideo = self._current_video
        newVideo = self._video_library.get_video(video_id)

        if newVideo != None:
            if oldVideo != None:
                print(f"Stopping video: {oldVideo.title}")
                print(f"Playing video: {newVideo.title}")
                self._current_video = newVideo
                self._paused_video = 0
            else:
                self._current_video = newVideo
                print(f"Playing video: {newVideo.title}")
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if self._current_video != None:
            oldVideo = self._current_video 
            print(f"Stopping video: {oldVideo.title}")
            self._current_video = None
            self._paused_video = 0
        else:
            print("Cannot stop video: No video is currently playing")


    def play_random_video(self):
        """Plays a random video from the video library."""
        if self._current_video != None:
            VideoPlayer.stop_video(self)
        rawVideos = self._video_library.get_all_videos()
        num_videos = len(rawVideos)
        random_video = randint(0, num_videos-1)
        VideoPlayer.play_video(self, rawVideos[random_video].video_id)
        


    def pause_video(self):
        """Pauses the current video."""
        if self._current_video == None:
            print("Cannot pause video: No video is currently playing")
        elif self._paused_video == 0:
            print(f"Pausing video: {self._current_video.title}")
            self._paused_video = 1
        else:
            print(f"Video already paused: {self._current_video.title}")


    def continue_video(self):
        """Resumes playing the current video."""
        if self._current_video == None:
            print("Cannot continue video: No video is currently playing")
        elif self._paused_video == 0:
            print("Cannot continue video: Video is not paused")
        else:
            print("Continuing video: Amazing Cats")
            self._paused_video == 0

    def show_playing(self):
        """Displays video currently playing."""
        if self._current_video == None:
            print("No video is currently playing")
        else:
            if self._paused_video == 0:
                print(f"Currently playing: {self._video_library.format(self._current_video)}")
            else:
                print(f"Currently playing: {self._video_library.format(self._current_video)} - PAUSED")

                

        

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if  self._playlists == []:
            self._playlists.append(video_playlist.Playlist(playlist_name, playlist_name.lower(), []))
            print(f"Successfully created new playlist: {playlist_name}")
        else:
            exists = video_library.VideoLibrary.playlist_in_list(self, playlist_name, self._playlists)
            if exists == False:
                self._playlists.append(video_playlist.Playlist(playlist_name, playlist_name.lower(), []))
                print(f"Successfully created new playlist: {playlist_name}")
            else:
                print("Cannot create playlist: A playlist with the same name already exists")
        

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        if video_library.VideoLibrary.playlist_in_list(self, playlist_name, self._playlists) == True:
            for num, playlist in enumerate(self._playlists):
                if playlist.playlist_id == playlist_name.lower():
                    if video_id not in playlist.videos:
                        if self._video_library.get_video(video_id) != None:
                            self._playlists[num].videos.append(video_id)
                            print(f"Added video to {playlist_name}: {self._video_library.get_video(video_id).title}")
                        else:
                            print(f"Cannot add video to {playlist_name}: Video does not exist")
                    else:
                        print(f"Cannot add video to {playlist_name}: Video already added")
        else:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")



    def show_all_playlists(self):
        """Display all playlists."""
        if self._playlists == []:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for playlist in self._playlists[::-1]:
                print(playlist.title)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if video_library.VideoLibrary.playlist_in_list(self, playlist_name, self._playlists) == True:
            for i, playlist in enumerate(self._playlists):
                if playlist_name.lower() == playlist.playlist_id:
                    index = i
            print(f"Showing playlist: {playlist_name}")
            if self._playlists[index].videos == []:
                print("No videos here yet")
            else:
                for video_ID in self._playlists[index].videos:
                    print(self._video_library.format(self._video_library.get_video(video_ID)))
        else:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """ 
        if video_library.VideoLibrary.playlist_in_list(self, playlist_name, self._playlists) == True:
            for i, playlist in enumerate(self._playlists):
                if playlist_name.lower() == playlist.playlist_id:
                    index = i
            video = self._video_library.get_video(video_id)
            if video != None:
                if video_id in self._playlists[index].videos:
                    video_index = self._playlists[index].videos.index(video_id)
                    del self._playlists[index].videos[video_index]
                    print(f"Removed video from {playlist_name}: {video.title}")
                else:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            else:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
        else:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if video_library.VideoLibrary.playlist_in_list(self, playlist_name, self._playlists) == True:
            for i, playlist in enumerate(self._playlists):
                if playlist_name.lower() == playlist.playlist_id:
                    index = i
            for video_index in range(0, len(self._playlists[index].videos)):
                del self._playlists[index].videos[video_index]
            print(f"Successfully removed all videos from {playlist_name}")
        else:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")


    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if video_library.VideoLibrary.playlist_in_list(self, playlist_name, self._playlists) == True:
            for i, playlist in enumerate(self._playlists):
                if playlist_name.lower() == playlist.playlist_id:
                    index = i
            del self._playlists[index]
            print(f"Deleted playlist: {playlist_name}")
        else:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")


    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        rawVideos = self._video_library.get_all_videos()
        searchedVideos = []
        for video in rawVideos:
            if search_term.lower() in video.title.lower():
                searchedVideos.append(video)
            else:
                continue
        if searchedVideos == []:
            print(f"No search results for {search_term}")
        else:
            print(f"Here are the results for {search_term}:")
            for i, video in enumerate(searchedVideos):
                print(f"{(i+1)}) {self._video_library.format(video)}]")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            choice = input("")
            try:
                VideoPlayer.play_video(self, searchedVideos[int(choice)-1].video_id)
            except:
                pass

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        rawVideos = self._video_library.get_all_videos()
        searchedVideos = []
        lower_video_tag = video_tag.lower()
        for video in rawVideos:
            for tag in video.tags:
                if lower_video_tag in tag.lower():
                    searchedVideos.append(video)
                else:
                    continue
        if searchedVideos == []:
            print(f"No search results for {video_tag}")
        else:
            print(f"Here are the results for {video_tag}:")
            for i, video in enumerate(searchedVideos):
                print(f"{(i+1)}) {self._video_library.format(video)}]")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            choice = input("")
            try:
                VideoPlayer.play_video(self, searchedVideos[int(choice)-1].video_id)
            except:
                pass


    def flag_video(self, video_ID, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

        video = self._video_library.get_video(video_ID)
        if video != None:
            for i, video_search in enumerate(self._all_videos):
                if video_search.video_id == video_ID:
                    index = i
            video = self._all_videos[index]
            if video.flagged == []:
                if flag_reason != "":
                    self._all_videos[index].flagged.append(flag_reason)
                    print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")
                else:
                    self._all_videos[index].flagged.append("Not supplied")
                    print(f"Successfully flagged video: {video.title} (reason: Not supplied)")
            else:
                print("Cannot flag video: Video is already flagged")
        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
