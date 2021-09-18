from Reddit.comment import *
from selenium.common.exceptions import StaleElementReferenceException
import random

# DEBUT CLASSE
class ScrapePost:

    browser = None
    question = None
    post = None
    comments = []

    #Constructor
    #@required browser
    def __init__(self, browser=None, question=None):
        self.question = question
        self.browser = browser

        waitPress('e')
        print('pressed e!')
        #self.sortTop()
        time.sleep(1)

        self.findPost()
        self.findQuestion()
        time.sleep(2)
        self.findComments()

    def findPost(self):
        self.post = self.browser.find_element_by_css_selector('#overlayScrollContainer > div.rhbaa2-0.dbNewH > div.rhbaa2-1.BiLZu > div')

    def findQuestion(self):
        if self.question is None:
            self.question = Comment(self.post.find_element_by_css_selector('div'), 0)
            self.question.createQuestion()
            print(self.question.print())

    def sortTop(self):
        #Finds the first button to click
        self.post.find_element_by_css_selector('#CommentSort--SortPicker > span').click()
        #Clicks on the TOP button
        self.browser.find_element_by_css_selector('#overlayScrollContainer > div.s1q45aff-0.hvehYm > a:nth-child(2) > button').click()


    def findComments(self):
        #commentsData = self.post.find_element_by_css_selector('div.p0SYO8TbZVqJIWEeFcNZx.ugs5wq-2.kwsbbM > div > div')
        commentsData = self.post.find_elements_by_css_selector('div.p0SYO8TbZVqJIWEeFcNZx.ugs5wq-2.kwsbbM > div > div > div > div')

        time.sleep(5)

        id = None

        for x in commentsData:
            try:
                if ('level' in x.text):
                    level = x.find_element_by_css_selector('div.s1m8d0lr-2.iDQVFl > span')
                    if level is not None:
                        levelText = level.text
                        if (levelText == 'level 1'):
                            id = random.randrange(100000000)
                            self.comments.append(Comment(x, 1, id))
                        elif (levelText == 'level 2'):
                            if self.comments[len(self.comments)-1].level == 1 and self.comments[len(self.comments)-1].id == id:
                                self.comments.append(Comment(x, 2, id))
                            else:
                                id = random.randrange(100000000)
                        elif (levelText == 'level 3'):
                            if self.comments[len(self.comments)-1].level == 2 and self.comments[len(self.comments)-1].id == id:
                                self.comments.append(Comment(x, 3, id))


            except StaleElementReferenceException as e:
                print(e)
                pass

        self.createComments()
        self.deleteUnwantedComments()
        self.createAudioAndImage()

    def createComments(self):
        for x in self.comments:
            x.createComment()


    def deleteUnwantedComments(self):
        for x in self.comments:
            if x.text is None:
                print("commentRemoved -> No text")
                self.comments.remove(x)
            elif x.wordCount > 500:
                print("commentRemoved -> " + str(x.wordCount) + " words")
                self.comments.remove(x)
            elif x.votes < 500:
                print("commentRemoved -> " + str(x.votes) + " votes")
                self.comments.remove(x)

    def createAudioAndImage(self):
        for i in range(len(self.comments)):
            self.comments[i].takeScreenshot(self.appropriateNumber(i+1))
            self.comments[i].makeTTS(self.appropriateNumber(i+1))
            time.sleep(.5)
            self.comments[i].makeClip(self.appropriateNumber(i+1))
            self.comments[i].print()

    def appropriateNumber(self, i):
        if i < 10:
            return str('00'+str(i))
        elif i < 100:
            return str('0'+str(i))
        else:
            return str(i)


#FIN CLASSE