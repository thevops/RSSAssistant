from time import sleep

from src.config import CONFIG, logger
from src.notifications import Notification
from src.RSSFeed import RSSFeed


def get_receiever_by_name(name):
    for receiver in CONFIG["receivers"]:
        if receiver["name"] == name:
            return receiver
    return None


def send_latest_feeds(**kwargs):
    name = kwargs["name"]
    logger.debug(f"{name} | start")
    url = kwargs["url"]
    history_limit = kwargs["history_limit"] if "history_limit" in kwargs else None
    receiver_name = kwargs["receiver"]
    # get receiver details by its name
    receiver = get_receiever_by_name(receiver_name)

    feed = RSSFeed(url, CONFIG["databaseDir"], history_limit)
    feed_items = feed.get_latest()
    logger.debug(f"{name} got items: {len(feed_items)}")

    for item in feed_items:
        logger.debug(
            f"Sending to {receiver['name']} | id={item['id']} title={item['title']} link={item['link']}"
        )
        s = Notification.notify(item, receiver)
        if s:
            logger.debug(
                f"Notification succeed with {receiver['name']} for {item['id']}"
            )
        else:
            logger.error(
                f"Notification failed with {receiver['name']} for {item['id']}"
            )

        # sleep for 0.5 seconds to avoid rate limiting
        sleep(0.5)

    logger.debug(f"{name} | finished")
