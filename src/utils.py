import os
import shutil
from .const import *


def clear_directory(directory) -> None:
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


def to_number(formatted_int) -> int:
    if formatted_int.endswith('k'):
        formatted_int = float(formatted_int.replace('k', ''))*1000
    return int(formatted_int)


def get_audio_len(path):
    audio_len = float(os.popen(
        f'{FFPROBE_PATH} -hide_banner -loglevel error -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {path}').read().replace('\n', ''))
    return audio_len
