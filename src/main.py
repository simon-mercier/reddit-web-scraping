from .scrapper import Scrapper

if __name__ == '__main__':
    reddit_post_url = "https://www.reddit.com/r/AskReddit/comments/prrkzj/what_is_an_item_you_think_should_be_free"
    scrapper = Scrapper(reddit_post_url)
    scrapper.scrape_post()
