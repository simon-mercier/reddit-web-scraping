from .scraper import scraper
import requests
from .const import *
import os
from dotenv import load_dotenv
import nltk


class VideoMaker(object):
    def __init__(self):
        load_dotenv(SRC_PATH / '.env')
        self.clean_repo()

    def generate_video(self) -> None:
        print("Generating video...")
        reddit_post_url = "https://www.reddit.com/r/AmItheAsshole/comments/ql79c7/aita_for_saying_if_my_sister_is_too_stupid_to/"

        def scrape_post():
            print(f"Scraping post @ {reddit_post_url}...")
            self.scraper = scraper(reddit_post_url)
            self.scraper.scrape_post(include_comments=False)

        def generate_comments():
            self.scraper.post.generate_audio()
            self.scraper.post.generate_subtitles()

            if hasattr(self.scraper.post, 'comments'):
                for comment in self.scraper.post.comments:
                    comment.generate_audio()
                    comment.generate_subtitles()

        def get_stock_videos():
            def get_noun_pharse():
                tokenized = nltk.word_tokenize(self.scraper.post.text)
                self.nouns = [word for (word, pos) in nltk.pos_tag(
                    tokenized) if(pos == 'NN')]
                if(len(self.nouns) == 0):
                    raise Exception(
                        "No nouns found in the post title. Please try again.")

            def get_pexels_api_results():
                print("Getting stock videos from Pexels API...")
                pexels_api_responses = []

                for noun in self.nouns:
                    search_videos_page = requests.get(
                        f"https://api.pexels.com/videos/search?query={noun}&per_page=80&page=1&orientation=portrait", headers={'Authorization': str(os.getenv('PEXELS_API_KEY')), 'Content-Type': 'application/json'})
                    pexels_api_responses.append(search_videos_page.json())

                self.sorted_api_responses = sorted(
                    pexels_api_responses, key=lambda x: x['total_results'], reverse=True)

            def download_pexels_videos():
                print("Downloading videos from Pexels API...")
                total_video_time = 0

                zipped_entries = []
                if(len(self.sorted_api_responses) == 0):
                    raise Exception(
                        "No videos found in the pexels api. Please try again.")
                elif(len(self.sorted_api_responses) == 1):
                    zipped_entries = list(
                        self.sorted_api_responses[0]['videos'])
                elif(len(self.sorted_api_responses) == 2):
                    zipped_entries = list(zip(
                        self.sorted_api_responses[0]['videos'], self.sorted_api_responses[1]['videos']))
                else:
                    zipped_entries = list(zip(
                        self.sorted_api_responses[0]['videos'], self.sorted_api_responses[1]['videos'], self.sorted_api_responses[2]['videos']))

                if(len(self.sorted_api_responses) != 1):
                    zipped_entries = [
                        item for sublist in zipped_entries for item in sublist]

                for index, video in enumerate(zipped_entries):
                    # get the video
                    data_url = 'https://www.pexels.com/video/' + \
                        str(video['id']) + '/download'
                    r = requests.get(data_url)

                    # download the video
                    with open(STOCK_VIDEO_PATH / f'stock_video_{index}_temp.mp4', 'wb') as outfile:
                        outfile.write(r.content)

                    # set the same video_track_time for all videos
                    os.system(
                        f'{FFMPEG_PATH} -hide_banner -loglevel error -i {STOCK_VIDEO_PATH / f"stock_video_{index}_temp.mp4"} -c copy -video_track_timescale 600 {STOCK_VIDEO_PATH / f"stock_video_{index}.mp4"}')
                    os.remove(STOCK_VIDEO_PATH /
                              f"stock_video_{index}_temp.mp4")

                    total_video_time += video['duration']

                    if(total_video_time > self.scraper.post.audio_len):
                        break

                print(f"Total video time: {total_video_time}")

            get_noun_pharse()
            get_pexels_api_results()
            download_pexels_videos()

        def join_audio():
            print("Joining audio...")
            audio_files = [str(COMMENTS_AUDIO_PATH / f) for f in os.listdir(
                COMMENTS_AUDIO_PATH) if f.endswith('.mp3')]
            if len(audio_files) == 0:
                raise Exception(
                    "No audio files found in the comments audio folder. Please try again.")

            joined_audio_files = '|'.join(audio_files)
            os.system(
                f'{FFMPEG_PATH} -hide_banner -loglevel error -i "concat:{joined_audio_files}" -acodec copy {POST_AUDIO_PATH / "post.mp3"} -map_metadata 0:1')

            def get_audio_time():
                self.scraper.post.audio_len = float(os.popen(
                    f'{FFPROBE_PATH} -hide_banner -loglevel error -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {POST_AUDIO_PATH / "post.mp3"}').read().replace('\n', ''))

                print(f"audio time: {self.scraper.post.audio_len}s")

            get_audio_time()

        def join_video():
            print("Joining videos...")

            video_files = ["echo file " + str(STOCK_VIDEO_PATH / f).replace('\\', '/') for f in os.listdir(
                STOCK_VIDEO_PATH) if f.endswith('.mp4')]

            os.system(
                f"({' & '.join(video_files)})>{STOCK_VIDEO_PATH / 'file_list.txt'}")
            os.system(
                f'{FFMPEG_PATH} -hide_banner -loglevel error -safe 0 -f concat -i {STOCK_VIDEO_PATH / "file_list.txt"} -c copy {POST_VIDEO_PATH / "post.mp4"}')

        def crop_video_to_9_16():
            print("Cropping video to 9:16... (this can take a while)")

            if not os.path.exists(POST_VIDEO_PATH / "post.mp4"):
                raise Exception(
                    "No video file found in the post video folder. Please try again.")

            os.system(
                f'{FFMPEG_PATH} -hide_banner -loglevel error -i {POST_VIDEO_PATH / "post.mp4"} -vf "crop=1080:1920" {POST_VIDEO_PATH / "post_cropped.mp4"}')
            os.remove(POST_VIDEO_PATH / "post.mp4")

        def join_video_and_audio():
            print("Joining video and audio...")
            os.system(
                f'{FFMPEG_PATH} -hide_banner -loglevel error -i {POST_VIDEO_PATH / "post_cropped.mp4"} -i {POST_AUDIO_PATH / "post.mp3"} -c:v copy -c:a aac -strict experimental {POST_VIDEO_PATH / "post_video_audio.mp4"}')
            os.remove(POST_VIDEO_PATH / "post_cropped.mp4")

        def trim_video():
            print("Trimming video...")
            os.system(
                f'{FFMPEG_PATH} -hide_banner -loglevel error -i {POST_VIDEO_PATH / "post_video_audio.mp4"} -ss 00:00:00 -t {self.scraper.post.audio_len} {POST_VIDEO_PATH / "post_trimmed.mp4"}')
            os.remove(POST_VIDEO_PATH / "post_video_audio.mp4")

        scrape_post()

        generate_comments()
        join_audio()

        get_stock_videos()
        join_video()
        crop_video_to_9_16()

        join_video_and_audio()
        trim_video()

    def clean_repo(self) -> None:
        for f in os.listdir(COMMENTS_AUDIO_PATH):
            os.remove(COMMENTS_AUDIO_PATH / f)
        for f in os.listdir(STOCK_VIDEO_PATH):
            os.remove(STOCK_VIDEO_PATH / f)
        for f in os.listdir(POST_AUDIO_PATH):
            os.remove(POST_AUDIO_PATH / f)
        for f in os.listdir(POST_VIDEO_PATH):
            os.remove(POST_VIDEO_PATH / f)
