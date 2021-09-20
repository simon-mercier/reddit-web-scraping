import os
from pathlib import Path
#DEBUT CLASSE
class ClipMaker:
    def __init__(self):
        self.root_path = Path(__file__).resolve().parent.parent
        self.ffmpeg_path = f"{self.root_path}/venv/site-packages/imageio_ffmpeg/binaries/ffmpeg-win32-v4.1.exe"
        self.assets_path = f"{self.root_path}/assets"
    def __call__(self, framerate, number):
        os.system(f"{self.ffmpeg_path} -r 5 -framerate {framerate} -s 1920x1080 -i {self.assets_path}/pictures/comment{number}.png -i {self.assets_path}/audio/tts{number}.mp3 -pix_fmt yuv420p -vcodec libx264 -acodec copy -y {self.assets_path}/clips/clip{number}.mp4")




#FIN CLASSE
