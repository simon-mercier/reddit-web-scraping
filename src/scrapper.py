from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from post import Post
from webdriver_manager.chrome import ChromeDriverManager as CM
from os import path
from const import *
from time import sleep
from comment import Comment


class Scrapper(object):
    def __init__(self, post_url):
        self.post_url = post_url
        self.start_browser()

    def start_browser(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")

        self.browser = webdriver.Chrome(
            executable_path=CM().install(), options=chrome_options)
        search_by_top = path.join(self.post_url, '?sort=top')
        self.browser.get(search_by_top)

    def scrape_post(self) -> None:
        def create_post():
            title = self.browser.find_element_by_xpath(
                '//*[@id="t3_prrkzj"]/div/div[3]/div[1]/div/h1').text
            author = self.browser.find_element_by_xpath(
                '//*[@id="t3_prrkzj"]/div/div[2]/div/div[1]/div/a').text
            self.post = Post(title, author, self.post_url)

        def create_comment() -> None:
            pass

        def is_valid_comment(comment) -> bool:
            pass

        def upvote_count(comment) -> int:
            pass

        def parse_top_comments() -> None:
            self.post.comments = []
            comment_count = 0

            comments = self.browser.find_elements_by_xpath(
                '//*[starts-with(@id,"t1_")]')

            while len(self.post.comments) < MAX_COMMENTS and comment_count < len(comments):
                current_comment = comments[comment_count]
                comment_count += 1

                if(upvote_count(current_comment) < MIN_NUMBER_VOTES_QUESTION):
                    break

                if(not is_valid_comment(current_comment)):
                    continue

                self.post.comments.append(create_comment(current_comment))

        create_post()
        parse_top_comments()
