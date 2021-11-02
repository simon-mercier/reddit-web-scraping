from .scraper import scraper
import requests
from .const import *
from pypexels import PyPexels
import os
from dotenv import load_dotenv
import nltk


class VideoMaker(object):
    def __init__(self):
        load_dotenv()
        self.py_pexel = PyPexels(api_key=os.getenv('PEXEL_API_KEY'))

    def generate_video(self) -> None:
        reddit_post_url = "https://www.reddit.com/r/AskReddit/comments/qemor9/if_brands_were_brutally_honest_what_brand_would"

        def scrape_page():
            self.scraper = scraper(reddit_post_url)
            self.scraper.scrape_post()

        def generate_comments():
            self.scraper.post.generate_audio()
            for comment in self.scraper.post.comments:
                comment.generate_audio()
                comment.generate_subtitles()

        def get_stock_videos():
            def get_noun_pharse():
                tokenized = nltk.word_tokenize(self.scraper.post.text)
                self.nouns = [word for (word, pos) in nltk.pos_tag(
                    tokenized) if(pos[:2] == 'NN')]
                if(len(self.nouns) == 0):
                    raise Exception(
                        "No nouns found in the post title. Please try again.")
                if DEBUG:
                    print(f"nouns in the post title: {self.nouns}")

            def get_pexels_api_results():
                pexels_api_responses = []

                for noun in self.nouns:
                    search_videos_page = self.py_pexel.videos_search(
                        query=noun, per_page=80, orientation="portrait")
                    pexels_api_responses.append(search_videos_page)

                self.pexels_best_response = max(
                    pexels_api_responses, key=lambda x: x.total_results)

                if DEBUG:
                    print(f"pexels best response: {self.pexels_best_response}")

            def download_pexels_videos():
                self.pexels_videos = []
                total_video_time = 0
                for index, video in enumerate(self.pexels_best_response.entries):
                    data_url = 'https://www.pexels.com/video/' + \
                        str(video.id) + '/download'
                    r = requests.get(data_url)
                    with open(STOCK_VIDEO_PATH / f'stock_video_{index}.mp4', 'wb') as outfile:
                        outfile.write(r.content)
                    total_video_time += video.duration

                    if(total_video_time > self.scraper.post.audio_len):
                        break

            get_noun_pharse()
            get_pexels_api_results()
            download_pexels_videos()

        def join_audio():
            audio_files = [str(COMMENTS_AUDIO_PATH / f) for f in os.listdir(
                COMMENTS_AUDIO_PATH) if f.endswith('.mp3')]
            joined_audio_files = '|'.join(audio_files)
            os.system(
                f'{FFMPEG_PATH} -hide_banner -loglevel error -i "concat:{joined_audio_files}" -acodec copy {POST_AUDIO_PATH / "post.mp3"} -map_metadata 0:1')

            # os.system(
            #     f'{FFPROBE_PATH} -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {POST_AUDIO_PATH / "post.mp3"}')
            # print(f"audio length: {self.scraper.post.audio_len}")

            def get_audio_time():
                self.scraper.post.audio_len = int(os.popen(
                    f'{FFPROBE_PATH} -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {POST_AUDIO_PATH / "post.mp3"}').read()
                )
                print(f"audio length: {self.scraper.post.audio_len}s")

            get_audio_time()

        def join_video():
            video_files = [str(STOCK_VIDEO_PATH / f) for f in os.listdir(
                STOCK_VIDEO_PATH) if f.endswith('.mp4')]
            joined_video_files = '|'.join(video_files)
            os.system(
                f'{FFMPEG_PATH} -hide_banner -loglevel error -i "concat:{joined_video_files}" -acodec copy {POST_VIDEO_PATH / "post.mp4"} -map_metadata 0:1')

        scrape_page()

        generate_comments()
        join_audio()

        get_stock_videos()
        join_video()

        self.clean_repo()

    def clean_repo(self) -> None:
        for f in os.listdir(COMMENTS_AUDIO_PATH):
            os.remove(COMMENTS_AUDIO_PATH / f)
        for f in os.listdir(STOCK_VIDEO_PATH):
            os.remove(STOCK_VIDEO_PATH / f)
        for f in os.listdir(POST_AUDIO_PATH):
            os.remove(POST_AUDIO_PATH / f)
        for f in os.listdir(POST_VIDEO_PATH):
            os.remove(POST_VIDEO_PATH / f)
