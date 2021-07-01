"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random
import numpy as np

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.current_playing = ""
        self.fl_playing_video = False
        self.playlists = []

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        videos = self._video_library.get_all_videos()
        titles = [video.title for video in videos]
        sorted_index = np.argsort(titles)

        print("Here's a list of all available videos:")
        for i in sorted_index:
            video = videos[i]
            tags = "[" + ' '.join(video.tags) + "]"
            video_info = video.title + " (" + video.video_id + ") " + tags
            if video.flagged_status:
                video_info += " - FLAGGED (reason: " + video.flag_reason + ")"
            print(video_info)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        library = self._video_library
        if video_id not in [vid.video_id for vid in library.get_all_videos()]:
            print("Cannot play video: Video does not exist")
        else:
            sel_video = library.get_video(video_id)
            if sel_video.flagged_status:
                print("Cannot play video: Video is currently flagged (reason: " + sel_video.flag_reason + ")")
            else:
                if self.current_playing == "":
                    print("Playing video: " + sel_video.title)
                    self.current_playing = video_id
                else:
                    print("Stopping video: " + library.get_video(self.current_playing).title)
                    print("Playing video: " + sel_video.title)
                    self.current_playing = video_id
                self.fl_playing_video = True


    def stop_video(self):
        """Stops the current video."""

        if self.current_playing == "":
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video: " + self._video_library.get_video(self.current_playing).title)
            self.current_playing = ""
            self.fl_playing_video = False

    def play_random_video(self):
        """Plays a random video from the video library."""

        library = self._video_library.get_all_videos()
        unflagged_videos = [v for v in library if not v.flagged_status]
        if unflagged_videos == []:
            print("No videos available")
        else:
            random_video = random.choice(unflagged_videos).video_id
            self.play_video(random_video)

    def pause_video(self):
        """Pauses the current video."""

        library = self._video_library
        if self.current_playing == "":
            print("Cannot pause video: No video is currently playing")
        else:
            if not self.fl_playing_video:
                print("Video already paused: " + library.get_video(self.current_playing).title)
            else:
                print("Pausing video: " + library.get_video(self.current_playing).title)
                self.fl_playing_video = False

    def continue_video(self):
        """Resumes playing the current video."""

        if self.current_playing == "":
            print("Cannot continue video: No video is currently playing")
        else:
            if not self.fl_playing_video:
                print("Continuing video: " + self._video_library.get_video(self.current_playing).title)
                self.fl_playing_video = True
            else:
                print("Cannot continue video: Video is not paused")


    def show_playing(self):
        """Displays video currently playing."""

        if self.current_playing == "":
            print("No video is currently playing")
        else:
            v = self._video_library.get_video(self.current_playing)
            paused_status = "" if self.fl_playing_video else " - PAUSED"
            tags = "[" + ' '.join(v.tags) + "]"
            video_info = v.title + " (" + v.video_id + ") " + tags
            print("Currently playing: " + video_info + paused_status)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.upper() not in [p.up_name for p in self.playlists]:
            new_playlist = Playlist(playlist_name)
            self.playlists.append(new_playlist)
            print("Successfully created new playlist: " + playlist_name)
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        library = self._video_library
        if playlist_name.upper() not in [p.up_name for p in self.playlists]:
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")
        else:
            if video_id not in [v.video_id for v in library.get_all_videos()]:
                print("Cannot add video to " + playlist_name + ": Video does not exist")
            else:
                sel_video = library.get_video(video_id)
                if sel_video.flagged_status:
                    print("Cannot add video to " + playlist_name + ": Video is currently flagged (reason: " + sel_video.flag_reason + ")")
                else:
                    index = (playlist_name.upper() == [p.up_name for p in self.playlists])
                    if video_id in self.playlists[index].videos:
                        print("Cannot add video to " + playlist_name + ": Video already added")
                    else:
                        print("Added video to " + playlist_name + ": " + library.get_video(video_id).title)
                        self.playlists[index].add_video(video_id)


    def show_all_playlists(self):
        """Display all playlists."""

        if len(self.playlists) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            playlist_names = [p.name for p in self.playlists]
            playlist_names.sort()
            for name in playlist_names:
                print(name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.upper() not in [p.up_name for p in self.playlists]:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")
        else:
            print("Showing playlist: " + playlist_name)
            index = (playlist_name.upper() == [p.up_name for p in self.playlists])
            if len(self.playlists[index].videos) == 0:
                print("No videos here yet")
            else:
                self.playlists[index].show_videos(self._video_library)

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        library = self._video_library
        if playlist_name.upper() not in [p.up_name for p in self.playlists]:
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")
        else:
            index = (playlist_name.upper() == [p.up_name for p in self.playlists])
            if video_id not in [v.video_id for v in library.get_all_videos()]:
                print("Cannot remove video from " + playlist_name + ": Video does not exist")
            else:
                if video_id not in self.playlists[index].videos:
                    print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
                else:
                    print("Removed video from " + playlist_name + ": " + library.get_video(video_id).title)
                    self.playlists[index].remove_video(video_id)

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in [p.up_name for p in self.playlists]:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")
        else:
            print("Successfully removed all videos from " + playlist_name)
            index = (playlist_name.upper() == [p.up_name for p in self.playlists])
            self.playlists[index].clear()

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in [p.up_name for p in self.playlists]:
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")
        else:
            print("Deleted playlist: " + playlist_name)
            index = (playlist_name.upper() == [p.up_name for p in self.playlists])
            del self.playlists[index]

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        library = self._video_library.get_all_videos()
        unflagged_videos = np.array([v for v in library if not v.flagged_status])
        titles = np.array([v.title for v in unflagged_videos])
        results = [(search_term.lower() in t.lower()) for t in titles]
        if sum(results) == 0:
            print("No search results for " + search_term)
        else:
            library2 = unflagged_videos[results]
            titles2 = titles[results]
            index = np.argsort(titles2)
            library2 = library2[index]
            print("Here are the results for " + search_term + ":")
            for i in range(len(library2)):
                v = library2[i]
                tags = "[" + ' '.join(v.tags) + "]"
                print(str(i+1) + ") " + v.title + " (" + v.video_id + ") " + tags)
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            answer = input()
            desired_inputs = np.array(range(1, len(library2)+1)).astype(str)
            if answer in desired_inputs:
                video_selected = library2[int(answer)-1]
                self.play_video(video_selected.video_id)


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        library = self._video_library.get_all_videos()
        unflagged_videos = np.array([v for v in library if not v.flagged_status])
        titles = np.array([v.title for v in unflagged_videos])
        hashtags = [v.tags for v in unflagged_videos]
        results = [(video_tag.lower() in t) for t in hashtags]
        if '#' not in video_tag or sum(results) == 0:
            print("No search results for " + video_tag)
        else:
            library2 = unflagged_videos[results]
            titles2 = titles[results]
            index = np.argsort(titles2)
            library2 = library2[index]
            print("Here are the results for " + video_tag + ":")
            for i in range(len(library2)):
                v = library2[i]
                tags = "[" + ' '.join(v.tags) + "]"
                print(str(i+1) + ") " + v.title + " (" + v.video_id + ") " + tags)
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            answer = input()
            desired_inputs = np.array(range(1, len(library2)+1)).astype(str)
            if answer in desired_inputs:
                video_selected = library2[int(answer)-1]
                self.play_video(video_selected.video_id)

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

        library = self._video_library.get_all_videos()
        ids = [v.video_id for v in library]
        if video_id not in ids:
            print("Cannot flag video: Video does not exist")
        else:
            index = ids.index(video_id)
            sel_video = library[index]
            if sel_video.flagged_status:
                print("Cannot flag video: Video is already flagged")
            else:
                self._video_library.flag_video(video_id, flag_reason)
                if self.current_playing != "" and self.current_playing == video_id:
                    print("Stopping video: " + sel_video.title)
                    self.current_playing = ""
                    self.fl_playing_video = False
                print("Successfully flagged video: " + sel_video.title + " (reason: " + sel_video.flag_reason + ")")



    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        library = self._video_library.get_all_videos()
        ids = [v.video_id for v in library]
        if video_id not in ids:
            print("Cannot remove flag from video: Video does not exist")
        else:
            index = ids.index(video_id)
            sel_video = library[index]
            if not sel_video.flagged_status:
                print("Cannot remove flag from video: Video is not flagged")
            else:
                self._video_library.allow_video(video_id)
                print("Successfully removed flag from video: " + sel_video.title)
