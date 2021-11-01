import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from .post import Post
from webdriver_manager.chrome import ChromeDriverManager as CM
from os import path
from .const import *
from time import sleep
from .comment import Comment
from .utils import *
from better_profanity import profanity


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

        sleep(5)

    def scrape_post(self) -> None:
        def create_post():
            title = self.browser.find_element_by_xpath(
                '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div[3]/div[1]/div/h1').text
            author = self.browser.find_element_by_xpath(
                '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/div/a').text
            upvotes = to_number(self.browser.find_element_by_xpath(
                '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div').text)
            self.post = Post(title, author, upvotes, self.post_url)

        def comment_has_target_level(comment: list) -> bool:
            return comment_level(comment) in TARGET_LEVELS

        def comment_text(comment: list) -> str:
            return comment[0].text

        def comment_level(comment: list) -> int:
            return int(re.search(r"\d+", comment[1].text)[0])

        def comment_upvotes(comment: list) -> int:
            return to_number(comment[2].text)

        def comment_has_enough_upvotes(comment) -> bool:
            return comment_upvotes(comment) > self.MIN_NUMBER_UPVOTES_QUESTION

        def comment_has_appropriate_char_count(comment) -> bool:
            return len(comment_text(comment)) < MAX_CHAR_COUNT_QUESTION

        def get_comments() -> list:

            comments_text = self.browser.find_elements_by_xpath(
                '/html/body/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div[2]/div[6]/div/div/div/div/div/div/div/div/div/div/div/p')
            comments_level = self.browser.find_elements_by_xpath(
                '/html/body/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div[2]/div[6]/div/div/div/div/div/div/div/div/div/span')
            comments_upvotes = self.browser.find_elements_by_xpath(
                '/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[6]/div/div/div/div/div/div/div/div/div/div[3]/div[1]')

            return list(zip(comments_text, comments_level,  comments_upvotes))

        def parse_top_comments() -> None:
            self.post.comments = []
            self.MIN_NUMBER_UPVOTES_QUESTION = self.post.upvotes * \
                MIN_NUMBER_UPVOTES_COMMENT_PERCENTAGE
            comment_count = 0

            comments = get_comments()

            skip_branch = False

            valid_comment_count = 0

            while len(self.post.comments) < MAX_COMMENTS and comment_count < len(comments):
                current_comment = comments[comment_count]
                comment_count += 1

                if(skip_branch and comment_level(current_comment) != 1):
                    continue

                skip_branch = True
                if(not comment_has_enough_upvotes(current_comment)):
                    if(comment_level(current_comment) == 1):
                        break
                    continue

                if(not comment_has_target_level(current_comment)):
                    continue

                if(not comment_has_appropriate_char_count(current_comment)):
                    continue

                if(profanity.contains_profanity(comment_text(current_comment))):
                    continue
                skip_branch = False

                valid_comment = Comment(comment_text(
                    current_comment), comment_level(current_comment), comment_upvotes(current_comment), valid_comment_count)
                valid_comment_count += 1

                self.post.comments.append(valid_comment)

        create_post()
        parse_top_comments()
