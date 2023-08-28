import signal

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config import CONFIG, logger, tz
from src.controller import send_latest_feeds

# Scheduler object
SCHEDULER = BlockingScheduler(timezone=tz)


def exit_handler(signal_received, frame):
    logger.info("Exiting gracefully")
    SCHEDULER.shutdown(wait=False)
    exit(0)


def main():
    logger.info("Starting RSSFeed")
    # Setup signal handlers
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    # Add jobs to scheduler
    for job in CONFIG["jobs"]:
        SCHEDULER.add_job(
            send_latest_feeds,
            trigger=CronTrigger.from_crontab(job["schedule"]),
            kwargs=job,
            max_instances=1,
            misfire_grace_time=60, # 1 minute
        )
        logger.info("Added RSSFeed job: %s" % job["name"])

    # Run schedulers infinite loop
    logger.info("Starting RSSFeed scheduler loop")
    SCHEDULER.start()


if __name__ == "__main__":
    main()
