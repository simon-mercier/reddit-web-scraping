
from pathlib import Path
from re import DEBUG

ROOT_PATH = Path(__file__).resolve().parent
FFMPEG_PATH = Path.joinpath(
    ROOT_PATH, "/venv/site-packages/imageio_ffmpeg/binaries/ffmpeg-win32-v4.1.exe")
ASSETS_PATH = Path.joinpath(ROOT_PATH, "/assets")

MIN_NUMBER_UPVOTES_COMMENT_PERCENTAGE = .1

MAX_COMMENTS = 20
MAX_PARSED_COMMENTS = 20

TARGET_LEVELS = [1, 2]

MAX_CHAR_COUNT_QUESTION = 300

DEBUG = True

TEMP_PATH = Path.joinpath(ROOT_PATH, "temp")

STOCK_VIDEO_PATH = Path.joinpath(TEMP_PATH, "stock_videos")
COMMENTS_MP3_PATH = Path.joinpath(TEMP_PATH, "comments_mp3")
