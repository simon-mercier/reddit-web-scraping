import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Reddit.scapePost import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


today = datetime.datetime.now()
minNumberOfVotesQuestion = 1000
minNumberOfVotesComment = 500

url = "https://www.reddit.com/"
url2 = "https://www.reddit.com/r/AskReddit/"
url3 = "https://www.reddit.com/r/Showerthoughts/"

removeFolders('C:/Users/mison/PycharmProjects/Robots/Reddit/Video/VideoClips')
removeFolders('C:/Users/mison/PycharmProjects/Robots/Reddit/Video/VideoScreenshots')
removeFolders('C:/Users/mison/PycharmProjects/Robots/Reddit/Video/VideoTTS')


#DEBUT CLASSE
class Initiate:

    nightMode = None

    #Constructor
    def __init__(self, nightMode = False):
        self.nightMode = nightMode

    def initiateBrowser(self):
        #Set incognito mode
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        #chrome_options.add_argument("--start-maximized")

        # Create browser
        self.browser = webdriver.Chrome(executable_path='C:/Users/mison/Documents/chromedriver_win32/chromedriver.exe', chrome_options=chrome_options)

        # Move the window to position x/y
        self.browser.set_window_size(1920,1080)
        self.browser.set_window_position(1920, 0)

        self.browser.get(url2)




        #Wait until it loads
        try:
            myElem = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'SHORTCUT_FOCUSABLE_DIV')))
            print("Page is ready!")
        except Exception:
            print("Loading took too much time!")


        #self.browser.set_window_size(3000, 800)

        #self.browser.execute_script("document.body.style.zoom='250%'")

        #self.browser.execute_script("document.body.style.zoom='200%'")

        if self.nightMode:
            self.nightMode()

        #Return the browser
        return self.browser

    def nightMode(self):
        # Activate dark mode
        self.browser.find_element_by_css_selector('#USER_DROPDOWN_ID > div > svg').click()
        self.browser.find_element_by_css_selector('body > div.o914k-17.iBDGto > button > button').click()

    def findFirstQuestion(self):
        #Find all the questions
        questionsData = self.browser.find_element_by_css_selector('#SHORTCUT_FOCUSABLE_DIV > div:nth-child(4) > div > div > div > div.th5f56-1.fJQRaL > div.th5f56-5.ftjuQd > div.sdccme-0.bSprja > div.rpBJOHq2PR60pnwJlUyP0.s1rcgrht-0.eEVuIz')

        #Find the first post to click on it
        firstQuestionData = questionsData.find_element_by_css_selector('div > div')
        firstQuestionData.click()
        firstQuestion = Comment(firstQuestionData, "Level 0")

        return firstQuestion

# FIN CLASSE

initiate = Initiate(False)
browser = initiate.initiateBrowser()
#firstQuestion = initiate.findFirstQuestion()


sP = ScrapePost(browser, None)

exit(0)