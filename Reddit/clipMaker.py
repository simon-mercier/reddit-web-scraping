import os

#DEBUT CLASSE
class ClipMaker:
    def __init__(self, framerate, number):
        os.system("C:/Users/mison/PycharmProjects/Robots/venv/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win32-v4.1.exe -r 5 -framerate "+ framerate +" -s 1920x1080 -i C:/Users/mison/PycharmProjects/Robots/Reddit/Video/VideoScreenshots/comment"+number+".png -i C:/Users/mison/PycharmProjects/Robots/Reddit/Video/VideoTTS/comment"+number+".mp3 -pix_fmt yuv420p -vcodec libx264 -acodec copy -y C:/Users/mison/PycharmProjects/Robots/Reddit/Video/VideoClips/clip"+number+".mp4")
#FIN CLASSE
