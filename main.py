from utils import *

if __name__ == '__main__':
    channel_url = input("Enter channel url: ")
    channel_id = get_channel_id_from_url(channel_url)
    path = input("Enter path save folder: ")
    download_youtube_videos(get_video_links(channel_id), path)
