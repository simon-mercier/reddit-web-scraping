import re
from gtts import gTTS
from .utils import *
from .const import *
from better_profanity import profanity
import pyttsx3
import cv2

USE_GTTS = True


class Comment:
    total_audio_len = 0

    def __init__(self, level, upvotes, number, text, title=None, author=None):
        self.text = text
        self.title = title
        self.author = author
        self.level = level
        self.upvotes = upvotes
        self.number = number

        self.clean_text()

    def clean_text(self):
        self.combined_text = self.title + '.' + self.text
        self.sanitize_text()
        self.seperated_text = re.split(
            r'\.+\s*|\?\s*|!\s*', self.combined_text)
        self.seperated_text = [i for i in self.seperated_text if i != '']

    def sanitize_text(self):
        def replace_all(text, dic):
            for i, j in dic.items():
                text = text.replace(i, j)
            return text

        self.combined_text = self.combined_text.lower()

        self.combined_text = replace_all(self.combined_text, {
            '\n': ' ', '\r': ' ', '\t': ' ', '\xa0': ' ', '\u200b': ' ', 'aita': 'am I the asshole'})

        self.combined_text = self.combined_text[:self.combined_text.find(
            'edit')]
        self.combined_text = self.combined_text[:self.combined_text.find(
            'info')]
        self.combined_text = self.combined_text[:self.combined_text.find(
            'tl;dr')]

    def generate_audio(self):
        self.audio_len = []

        for index, text in enumerate(self.seperated_text):
            if USE_GTTS:
                tts = gTTS(text, lang='en')
                tts.save(COMMENTS_AUDIO_PATH /
                         f'comment_{self.number}_part_{index+1}.mp3')
            else:
                engine = pyttsx3.init()
                engine.setProperty('rate', 120)
                engine.setProperty('volume', 1)
                engine.save_to_file(
                    self.combined_text, COMMENTS_AUDIO_PATH / f'comment_{self.number}_part_{index+1}.mp3')
                engine.runAndWait()
                engine.stop()

            self.audio_len.append(get_audio_len(
                COMMENTS_AUDIO_PATH / f'comment_{self.number}_part_{index+1}.mp3'))

            # self.total_audio_len += self.audio_len[index]

    def generate_subtitles(self):
        current_audio_len = 0
        for index, text in enumerate(self.seperated_text):
            sanitized_text = profanity.censor(text, censor_char='*')

            def write_text_on_video(text, subtitle_path, start_time, end_time):
                subtitle = open(subtitle_path, 'a')
                subtitle.write(f'{index+1}\n')
                subtitle.write(f'{start_time} --> {end_time}\n')
                subtitle.write(f'{text}\n\n')
                subtitle.close()

            new_audio_len = current_audio_len + self.audio_len[index]
            write_text_on_video(sanitized_text, POST_SUBTITLE_PATH /
                                f'post.srt', current_audio_len, new_audio_len)
            current_audio_len = new_audio_len
