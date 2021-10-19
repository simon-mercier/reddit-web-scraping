
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent
FFMPEG_PATH = f"{ROOT_PATH}/venv/site-packages/imageio_ffmpeg/binaries/ffmpeg-win32-v4.1.exe"
ASSETS_PATH = f"{ROOT_PATH}/assets"

MIN_NUMBER_VOTES_QUESTION = 10000
MIN_NUMBER_VOTES_COMMENT_PERCENTAGE = .1

MAX_COMMENTS = 5
MAX_PARSED_COMMENTS = 20

DEBUG = True
