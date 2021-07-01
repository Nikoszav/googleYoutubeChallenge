"""A video playlist class."""
from .video_library import VideoLibrary

class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name):
    	self.name = name
    	self.up_name = name.upper()
    	self.videos = []

    def add_video(self, video_id):
    	self.videos.append(video_id)

    def remove_video(self, video_id):
    	self.videos.remove(video_id)

    def show_videos(self, library):
    	for video in self.videos:
            newVideo = library.get_video(video)
            tags = "[" + ' '.join(newVideo.tags) + "]"
            video_info = newVideo.title + " (" + newVideo.video_id + ") " + tags
            if newVideo.flagged_status:
                video_info = video_info + " - FLAGGED (reason: " + newVideo.flag_reason + ")"
            print(video_info)

    def clear(self):
    	self.videos.clear()
