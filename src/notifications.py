import datetime
import json
import re
import tempfile

import apprise
from json_dict_transformer import translateDictToDict
from pytube import YouTube
from todoist_api_python.api import TodoistAPI

from src.config import logger


class TransformFunctions:
    def remove_html_tags(text):
        """
        Remove HTML tags from text
        """
        clean = re.compile("<.*?>")
        return re.sub(clean, "", text)

    def youtube_video_length(video_url):
        """
        Get the length of a YouTube video.
        Return video URL and length in format: URL (HH:MM:SS)
        """
        try:
            yt = YouTube(video_url)
            duration = str(datetime.timedelta(seconds=yt.length))
        except Exception as e:
            logger.error(f"Cannot get length of {video_url}: {e}")
            return video_url

        return f"{video_url} ({duration})"


class Notification:
    @staticmethod
    def notify(item_, receiver):
        """
        Wrapper for all notification types
        """
        # Transform item using template
        if "transform_schema" in receiver:
            schema = json.loads(receiver["transform_schema"])
            item = translateDictToDict(item_, schema, TransformFunctions)
        else:
            item = item_

        if receiver["type"] == "discord":
            return Notification.discord(item, receiver)
        elif receiver["type"] == "echo":
            return Notification.echo(item, receiver)
        elif receiver["type"] == "todoist":
            return Notification.todoist(item, receiver)
        else:
            return False

    @staticmethod
    def echo(item, _):
        """
        Send a notification to the console
        """
        print(f"Title: {item['title']}")
        print(f"Body: {item['body']}")
        return True

    @staticmethod
    def discord(item, receiver):
        """
        Send a notification to Discord
        https://github.com/caronc/apprise/wiki/Notify_discord
        """
        title = item["title"]
        body = item["body"]
        url = receiver["url"]

        apobj = apprise.Apprise()
        apobj.add(url)

        # Discord has a limit of 2000 characters per message
        # We use 1900 to be on the safe side
        if len(body) < 1900:
            # Send a notification as a plain text
            status = apobj.notify(title=title, body="```" + body + "```")
            if not status:
                return False
        else:
            # Send a notification as a text file
            f = tempfile.NamedTemporaryFile(mode="w", suffix=".txt")
            f.write(body)
            f.flush()  # Immediately flush data to the file.
            status = apobj.notify(title=title, body="", attach=f.name)
            f.close()  # Close and delete the file
            if not status:
                return False

        return True

    @staticmethod
    def todoist(item, receiver):
        title = item["title"]
        body = item["body"]
        token = receiver["token"]
        project_id = receiver["project_id"] if "project_id" in receiver else None
        section_id = receiver["section_id"] if "section_id" in receiver else None

        try:
            api = TodoistAPI(token)
            api.add_task(
                content=title,
                description=body,
                project_id=project_id,
                section_id=section_id,
            )
        except Exception as error:
            logger.error(f"Cannot add task {title}: {error}")
            return False
