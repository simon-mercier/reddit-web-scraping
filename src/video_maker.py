from .scraper import scraper
import requests
from .const import *
from .utils import *
import os
from dotenv import load_dotenv
import nltk


class VideoMaker(object):
    def __init__(self, post_url: str):
        load_dotenv(SRC_PATH / '.env')
        self.post_url = post_url
        self.clean_temp()

    def generate_video(self, keywords=None) -> None:
        print("Generating video...")

        def scrape_post():
            print(f"Scraping post @ {self.post_url}...")
            self.scraper = scraper(self.post_url)
            self.scraper.scrape_post()

        def generate_comments():
            self.scraper.post.generate_audio()

        def get_stock_videos(keywords):
            def get_search_words():
                tokenized = nltk.word_tokenize(self.scraper.post.text)
                self.words_to_search = [word for (word, pos) in nltk.pos_tag(
                    tokenized) if(pos == 'NN')]
                if(len(self.words_to_search) == 0):
                    raise Exception(
                        "No nouns found in the post title. Please try again.")

            def get_pexels_api_results():
                print("Getting stock videos from Pexels API...")
                pexels_api_responses = []

                for word in self.words_to_search:
                    search_videos_page = requests.get(
                        f"https://api.pexels.com/videos/search?query={word}&per_page=80&page=1&orientation=portrait", headers={'Authorization': str(os.getenv('PEXELS_API_KEY')), 'Content-Type': 'application/json'})
                    pexels_api_responses.append(search_videos_page.json())

                self.sorted_api_responses = sorted(
                    pexels_api_responses, key=lambda x: x['total_results'], reverse=True)

                self.sorted_api_responses = [
                    x for x in self.sorted_api_responses if(x['total_results'] > 0)]

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

                    if(total_video_time > self.scraper.post.total_audio_len):
                        break

                print(f"Total video time: {total_video_time}")

            if(keywords is None):
                get_search_words()
            else:
                self.words_to_search = keywords

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

            self.scraper.post.total_audio_len = get_audio_len(
                POST_AUDIO_PATH / "post.mp3")

        def join_video():
            print("Joining videos...")
            if(len(os.listdir(STOCK_VIDEO_PATH)) == 0):
                raise Exception(
                    "No videos found in the stock video folder. Please try again.")

            video_files = ["echo file " + str(STOCK_VIDEO_PATH / f).replace('\\', '/') for f in os.listdir(
                STOCK_VIDEO_PATH) if f.endswith('.mp4')]

            os.system(
                f"({' & '.join(video_files)})>{STOCK_VIDEO_PATH / 'file_list.txt'}")
            os.system(
                f'{FFMPEG_PATH} -hide_banner -loglevel error -safe 0 -f concat -i {STOCK_VIDEO_PATH / "file_list.txt"} -i {POST_AUDIO_PATH / "post.mp3"} -c:v copy -c:a aac -strict experimental {POST_VIDEO_PATH / "post.mp4"}')

        def crop_video_to_9_16():
            print("Cropping video to 9:16... (this could take a while)")

            if not os.path.exists(POST_VIDEO_PATH / "post.mp4"):
                raise Exception(
                    "No video file found in the post video folder. Please try again.")

            os.system(
                f'{FFMPEG_PATH} -hide_banner -loglevel error -i {POST_VIDEO_PATH / "post.mp4"} -vf "crop=1080:1920" {POST_VIDEO_PATH / "post_cropped.mp4"}')

        def trim_video():
            print("Trimming video...")
            os.system(
                f'{FFMPEG_PATH} -hide_banner -loglevel error -i {POST_VIDEO_PATH / "post_cropped.mp4"} -ss 00:00:00 -t {self.scraper.post.total_audio_len} {POST_VIDEO_PATH / "post_trimmed.mp4"}')

        def generate_subtitles():
            print("Generating subtitles...")
            self.scraper.post.generate_subtitles()

        def join_subtitles_ffmpeg():
            # os.system(
            #     f'{FFMPEG_PATH} -i {POST_VIDEO_PATH / "post.mp4"} -vf "drawtext=fontfile=/Code/reddit-web-scraping/src/assets/fonts/ProximaNova_Regular.otf:textfile=/Code/reddit-web-scraping/src/temp/post_subtitle/post.srt:reload=1:fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h)/2" -codec:a copy {POST_VIDEO_PATH / "post_with_subtitles.mp4"}')
            # # os.system(
            #     f'{FFMPEG_PATH} -i {POST_VIDEO_PATH / "post.mp4"} -vf "drawtext=fontfile={str(ASSETS_PATH).replace("C", "") + f"{chr(92)}ProximaNova_Regular.otf"}:textfile={str(POST_SUBTITLE_PATH).replace("C:", "")  + f"{chr(92)}post.srt"}:reload=1:fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h)/2" -codec:a copy {POST_VIDEO_PATH / "post_with_subtitles.mp4"}')
            # os.system(f'{FFMPEG_PATH} -i {POST_VIDEO_PATH / "post.mp4"} -filter_complex "subtitles=/Code/reddit-web-scraping/src/temp/post_subtitle/post.srt" -c:v libx264 -crf 20 -c:a aac -strict experimental -b:a 192k {POST_VIDEO_PATH / "post_with_subtitles.mp4"}')
            pass

        scrape_post()

        generate_comments()
        join_audio()

        get_stock_videos(keywords)

        join_video()
        # crop_video_to_9_16()
        # trim_video()

        generate_subtitles()
        join_subtitles_ffmpeg()

    def clean_temp(self) -> None:
        for f in os.listdir(COMMENTS_AUDIO_PATH):
            os.remove(COMMENTS_AUDIO_PATH / f)
        for f in os.listdir(STOCK_VIDEO_PATH):
            os.remove(STOCK_VIDEO_PATH / f)
        for f in os.listdir(POST_AUDIO_PATH):
            os.remove(POST_AUDIO_PATH / f)
        for f in os.listdir(POST_VIDEO_PATH):
            os.remove(POST_VIDEO_PATH / f)
