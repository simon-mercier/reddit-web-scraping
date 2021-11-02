from gtts import gTTS
from .utils import *
from .const import *


class Comment:
    def __init__(self, text, level, upvotes, number):
        self.text = text
        self.level = level
        self.upvotes = upvotes
        self.number = number

    def print(self):
        if DEBUG and self.text is not None:
            print("\n[#START COMMENT")
            print("Level = " + str(self.level))
            print("Text = " + self.text)
            print("Word Count = " + str(self.wordCount))
            print("Votes = " + str(self.votes) + "\n#END COMMENT]")

    def generate_audio(self):
        tts = gTTS(text=self.text, lang='en', tld='ca')
        tts.save(COMMENTS_AUDIO_PATH / f"comment_{self.number}.mp3")

    def generate_subtitles(self):
        pass
