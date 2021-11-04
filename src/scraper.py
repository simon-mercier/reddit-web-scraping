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

    def scrape_post(self) -> None:
        def create_post():
            title = self.page.find(
                'h1', {'class': '_eYtD2XCVieq6emjKBH3m'}).text

            text = self.page.find(
                'div', {'class': '_292iotee39Lmt0MkQZ2hPV'}).text

            upvotes = to_number(self.page.find(
                'div', {'class': '_1E9mcoVn4MYnuBQSVDt1gC'}).text)

            self.post = Comment(level=0, number=0, title=title,
                                text=text, upvotes=upvotes, author=None)

        create_post()
