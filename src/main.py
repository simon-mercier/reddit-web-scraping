from .scrapper import Scrapper

if __name__ == '__main__':
    reddit_post_url = "https://www.reddit.com/r/AskReddit/comments/qemor9/if_brands_were_brutally_honest_what_brand_would"
    scrapper = Scrapper(reddit_post_url)
    scrapper.scrape_post()
