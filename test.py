from src.config import CONFIG
from src.controller import send_latest_feeds
from src.RSSFeed import RSSFeed
from src.notifications import Notification


# TEST FUNCTIONS
def test_RSSFeed_1():
    feed_url = "https://www.reddit.com/r/Python/new/.rss"
    feed = RSSFeed(feed_url)
    feed_items = feed.parse()
    for item in feed_items:
        print(f"{item['id']}: {item['title']} {item['link']}")


def test_RSSFeed_2():
    feed_url = "https://lorem-rss.herokuapp.com/feed?unit=second&interval=30&length=2"
    feed = RSSFeed(feed_url, "db/", history_limit=3)
    feed_items = feed.get_latest()
    for item in feed_items:
        print(f"id={item['id']} title={item['title']} link={item['link']}")


def test_RSSFeed_3():
    feed_url = "https://cloud.google.com/feeds/gke-main-release-notes.xml"
    feed = RSSFeed(feed_url, "db/", history_limit=10)
    feed_items = feed.parse()
    for item in feed_items:
        print(f"id={item['id']} title={item['title']} link={item['link']}")


def test_full_1():
    for job in CONFIG["jobs"]:
        send_latest_feeds(**job)

def test_http_request():
    url = "https://hook.eu2.make.com/....."
    item = {
        "title": "This is an example task",
        "body": "With an example body content"
    }
    receiver = {
        "type": "http_request",
        "url": url
    }
    Notification.http_request(item, receiver)


# RUN TESTS
# test_RSSFeed_1()
# test_RSSFeed_2()
# test_RSSFeed_3()
# test_full_1()
test_http_request()
