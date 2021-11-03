import re
from bs4 import BeautifulSoup as soup
from os import path
from .const import *
from time import sleep
from .comment import Comment
from .utils import *
from better_profanity import profanity
import requests


class scraper(object):
    def __init__(self, post_url):
        self.post_url = post_url
        self.start_browser()

    def start_browser(self) -> None:

        search_by_top = path.join(self.post_url, '?sort=top')
        headers = {
            'User-Agent': 'Chrome/51.0.2704.103 Safari/537.36'}
        source = requests.get(search_by_top, headers=headers)
        self.page = soup(source.text, "html.parser")

    def scrape_post(self, include_comments: bool) -> None:
        def create_post():
            title = self.page.find(
                'h1', {'class': '_eYtD2XCVieq6emjKBH3m'}).text

            text = self.page.find(
                'div', {'class': '_292iotee39Lmt0MkQZ2hPV'}).text

            upvotes = to_number(self.page.find(
                'div', {'class': '_1E9mcoVn4MYnuBQSVDt1gC'}).text)

            self.post = Comment(level=0, number=0, title=title,
                                text=text, upvotes=upvotes, author=None)

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

            comments_text = self.page.find_all(
                'div', {'class': '_1qeIAgB0cPwnLhDF9XSiJM'}).text
            comments_level = self.page.find_all(
                'div', {'class': '_1RIl585IYPW6cmNXwgRz0J'}).text
            comments_upvotes = self.page.find_all(
                'div', {'class': '_1E9mcoVn4MYnuBQSVDt1gC'}).text
            comments_upvotes = comments_upvotes[1:]

            return list(zip(comments_text, comments_level,  comments_upvotes))

        def scrape_comments() -> None:
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

                valid_comment_count += 1
                valid_comment = Comment(text=comment_text(
                    current_comment), level=comment_level(current_comment), upvotes=comment_upvotes(current_comment), number=valid_comment_count)

                self.post.comments.append(valid_comment)

        create_post()
        if(include_comments):
            scrape_comments()
