# from gtts import gTTS
from .utils import *
# from PIL import Image
# from mutagen.mp3 import MP3
# from clipMaker import *
from .const import *


class Comment:
    def __init__(self, text, level, upvotes):
        self.text = text
        self.level = level
        self.upvotes = upvotes

    def print(self):
        if DEBUG and self.text is not None:
            print("\n[#START COMMENT")
            print("Level = " + str(self.level))
            print("Text = " + self.text)
            print("Word Count = " + str(self.wordCount))
            print("Votes = " + str(self.votes) + "\n#END COMMENT]")

    # def createQuestion(self):
    #     self.text = self.text.find_element_by_css_selector(
    #         'h2.s1okktje-0.eYgaub').text
    #     if self.text is not None:
    #         self.setName()
    #         self.wordCount = len(self.text.split())
    #         self.votes = re.sub(
    #             r"\.\d+k", "000", self.text.find_element_by_css_selector('div._1rZYMD_4xY3gRcSS3p8ODO').text)
    #         self.votes = re.sub(r"Score hidden", "1001", self.votes)
    #         self.votes = int(self.votes)
    #         self.takeScreenshot('000')
    #         self.makeTTS('000')
    #         self.makeClip('000')

    # def createComment(self):
    #     self.text = self.text.find_element_by_css_selector(
    #         'div.fo16tt-0.bJBAtI').text
    #     if self.text is not None:
    #         self.setName()
    #         self.wordCount = len(self.text.split())
    #         self.votes = re.sub(
    #             r"\.\d+k\spoints", "000", self.text.find_element_by_css_selector('span.h5svje-0.cFQOcm').text)
    #         self.votes = re.sub(r"points", "", self.votes)
    #         self.votes = re.sub(r"Score hidden", "101", self.votes)
    #         self.votes = int(self.votes)

    # def setName(self):
    #     if self.text is not None:
    #         '''
    #         if len(self.text.split()) < 3:
    #             self.name = re.match(r"([^\s]+)", self.text).group(0)
    #         elif len(self.text.split()) < 5:
    #             self.name = re.match(r"([^\s]+) ([^\s]+) ([^\s]+)", self.text).group(0)
    #         else:
    #             self.name = re.match(r"([^\s]+) ([^\s]+) ([^\s]+) ([^\s]+) ([^\s]+)", self.text).group(0)
    #         '''
    #         self.name = self.text[: min(15, len(self.text)-1)]
    #         self.name = re.sub(r"(\W+)", "-", self.name)

    # def takeScreenshot(self, number):
    #     if self.text is not None:
    #         self.screenshot = self.text.screenshot(
    #             self.path[0] + "comment" + number + ".png")
    #         img = Image.open(self.path[0] + "comment" + number + ".png")
    #         img = img.resize(
    #             ((self.text.size['width']*2), (self.text.size['height']*2)), Image.ANTIALIAS)
    #         img_w, img_h = img.size
    #         background = Image.new('RGBA', (1920, 1080), (255, 255, 255, 255))
    #         bg_w, bg_h = background.size
    #         offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    #         background.paste(img, offset)
    #         background.save(self.path[0] + "comment" + number + ".png", "png")

    # def makeTTS(self, number):
    #     if self.text is not None:
    #         self.speech = gTTS(text=self.text, lang='en')
    #         self.speech.save(self.path[1] + "comment" + number + ".mp3")

    # def makeClip(self, number):
    #     time.sleep(.5)
    #     clip = ClipMaker(str(
    #         (1 / MP3(self.path[1] + "comment" + number + ".mp3").info.length) + 1), number)
