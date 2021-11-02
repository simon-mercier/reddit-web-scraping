
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent

SRC_PATH = ROOT_PATH / 'src'

FFMPEG_PATH = ROOT_PATH / "venv" / \
    "Lib" / "site-packages" / "ffmpeg" / "bin" / "ffmpeg.exe"

FFPROBE_PATH = ROOT_PATH / "venv" / \
    "Lib" / "site-packages" / "ffmpeg" / "bin" / "ffprobe.exe"

ASSETS_PATH = ROOT_PATH / "assets"

TEMP_PATH = SRC_PATH / 'temp'

STOCK_VIDEO_PATH = TEMP_PATH / 'stock_video'

POST_VIDEO_PATH = TEMP_PATH / 'post_video'

COMMENTS_AUDIO_PATH = TEMP_PATH / 'comments_audio'

POST_AUDIO_PATH = TEMP_PATH / 'post_audio'

MIN_NUMBER_UPVOTES_COMMENT_PERCENTAGE = .1

MAX_COMMENTS = 20
MAX_PARSED_COMMENTS = 20

TARGET_LEVELS = [1]

MAX_CHAR_COUNT_QUESTION = 300

DEBUG = True
