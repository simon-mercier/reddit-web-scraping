import os
import const


class ClipMaker:
    def __call__(self, framerate, number):
        os.system(f"{const.FFMPEG_PATH} -r 5 -framerate {framerate} -s 1920x1080 -i {const.ASSETS_PATH}/pictures/comment{number}.png -i {const.ASSETS_PATH}/audio/tts{number}.mp3 -pix_fmt yuv420p -vcodec libx264 -acodec copy -y {const.ASSETS_PATH}/clips/clip{number}.mp4")
