from pytube import YouTube
from pytube.exceptions import VideoUnavailable, PytubeError
import scrapetube


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


if __name__ == '__main__':
    channel = "UCau7fBZr_fSNb4CzbGWA1Rw"
    path = "/Users/avixiii/Desktop/videos"
    download_youtube_videos(get_video_links(channel), path)

