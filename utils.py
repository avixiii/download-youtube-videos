from pytube import YouTube
from pytube.exceptions import VideoUnavailable, PytubeError
import scrapetube
import requests
from bs4 import BeautifulSoup
import re


def get_channel_id_from_url(channel_url):
    response = requests.get(channel_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the script containing channel information
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:  # Check if script.string is not None
                match = re.search(r'"channelId":"([^"]+)"', script.string)
                if match:
                    return match.group(1)

    return None


def get_video_links(channel_id):
    videos = scrapetube.get_channel(channel_id)
    urls = []
    for video in videos:
        urls.append("https://www.youtube.com/watch?v=" + str(video['videoId']))

    return urls


def download_youtube_videos(links, save_path):
    for link in links:
        try:
            yt = YouTube(link)
        except VideoUnavailable:
            print(f"The video at the link {link} is unavailable.")
            continue
        except PytubeError as e:
            print(f"An error occurred while fetching video details for {link}: {e}")
            continue

        # Get the video streams
        streams = yt.streams.filter(progressive=True, file_extension="mp4")

        # Get the highest resolution video stream
        video_stream = streams.get_highest_resolution()
        try:
            # Download the video
            video_stream.download(output_path=save_path)
            print(f"Downloaded: {yt.title}")
        except FileNotFoundError:
            print(f"Failed to save the downloaded video for {yt.title}. Check the save path.")
        except Exception as e:
            print(f"An error occurred while downloading {yt.title}: {e}")

    print('Task Completed!')
