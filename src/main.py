from .video_maker import VideoMaker

if __name__ == '__main__':
    video_maker = VideoMaker(
        "https://www.reddit.com/r/AmItheAsshole/comments/qlf77y/aita_for_throwing_a_party_for_my_daughters_after/")
    video_maker.generate_video('party')
