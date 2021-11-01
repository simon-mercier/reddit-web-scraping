from .scrapper import Scrapper
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
            self.scrapper = Scrapper(reddit_post_url)
            self.scrapper.scrape_post()

        def get_stock_videos():
            def get_noun_pharse():
                tokenized = nltk.word_tokenize(self.scrapper.post.title)
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
                        query=noun, per_page=15, orientation="portrait")
                    pexels_api_responses.append(search_videos_page)

                self.pexels_best_response = max(
                    pexels_api_responses, key=lambda x: x.total_results)

                if DEBUG:
                    print(f"pexels best response: {self.pexels_best_response}")

            def download_pexels_videos():
                self.pexels_videos = []
                for index, video in enumerate(self.pexels_best_response.entries):
                    print(video.id, video.user.get('name'), video.url)
                    data_url = 'https://www.pexels.com/video/' + \
                        str(video.id) + '/download'
                    r = requests.get(data_url)
                    with open(Path.joinpath(STOCK_VIDEO_PATH, f'stock_video_{index}.mp4'), 'wb') as outfile:
                        outfile.write(r.content)

            get_noun_pharse()
            get_pexels_api_results()
            download_pexels_videos()

        def combine_mp3_videos():
            pass

        def combine_mp4_videos():
            pass

        def generate_comments_videos():
            for comment in self.scrapper.post.comments:
                comment.generate_mp3()
                comment.generate_subtitles()

        scrape_page()

        generate_comments_videos()
        combine_mp3_videos()

        get_stock_videos()
        combine_mp4_videos()
