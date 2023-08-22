import hashlib
import os

import feedparser
import pickledb


class RSSFeed:
    def __init__(self, link, database_dir="db/", history_limit=100):
        self.link = link
        self.history_limit = history_limit
        # File name for storing the database is separate for each link
        # The name is created by hashing the link
        self.database_path = (
            database_dir + hashlib.md5(link.encode("utf-8")).hexdigest() + ".db.json"
        )

        # Check if the database file exists
        # If so, it is NOT the first run
        if os.path.exists(self.database_path):
            self.first_run = False
        else:
            self.first_run = True

    def pull(self):
        return feedparser.parse(self.link)

    def parse(self):
        feed = self.pull()
        feeds = []
        for entry in feed.entries:
            # entry obligatory contains: id, title, link
            # rest is optional
            feeds.append(entry)
        return feeds

    def load_database(self):
        # sig=False is needed to avoid error:
        # ValueError: signal only works in main thread of the main interpreter
        return pickledb.load(self.database_path, auto_dump=False, sig=False)

    def clean_database(self):
        db = self.load_database()
        for item in db.getall():
            item_data = db.get(item)
            while len(item_data) > self.history_limit:
                item_data.pop(0)
            # overwrite the old list with the new one
            db.set(item, item_data)
            db.dump()

    def get_latest(self):
        feed_items = self.parse()
        db = self.load_database()
        latest = []

        # self.link is a key containing list of IDs
        if db.exists(self.link):
            # get list of IDs for the link
            link_ids = db.get(self.link)
            for item in feed_items:
                if item["id"] not in link_ids:
                    latest.append(item)
                    link_ids.append(item["id"])
            # save new ID list for link
            db.set(self.link, link_ids)

        else:
            # create new list of IDs for the link
            link_ids = []
            for item in feed_items:
                link_ids.append(item["id"])
            db.set(self.link, link_ids)
            latest = feed_items

        # save the database
        db.dump()

        # clean the database by removing old IDS
        self.clean_database()

        # Return latest only if it is NOT the first run
        if self.first_run:
            return []
        else:
            return latest
