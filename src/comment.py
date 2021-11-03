from gtts import gTTS
from .utils import *
from .const import *
from better_profanity import profanity
import pyttsx3

USE_GTTS = True


class Comment:
    def __init__(self, level, upvotes, number, text, title=None, author=None):
        self.text = text
        self.title = title
        self.author = author
        self.level = level
        self.upvotes = upvotes
        self.number = number

    def generate_audio(self):
        sanitized_text = profanity.censor(
            self.title+self.text, censor_char=' ')

        def replace_all(text, dic):
            for i, j in dic.items():
                text = text.replace(i, j)
            return text

        if USE_GTTS:
            tts = gTTS(text=sanitized_text, lang='en')
            tts.save(COMMENTS_AUDIO_PATH / f'comment_{self.number}.mp3')
        else:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.save_to_file(
                sanitized_text, COMMENTS_AUDIO_PATH / f'comment_{self.number}.mp3')
            engine.runAndWait()
            engine.stop()

    def generate_subtitles(self):
        sanitized_text = profanity.censor(self.text, censor_char='*')
