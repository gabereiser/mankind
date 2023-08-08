from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from asyncio import get_event_loop
from datetime import datetime as dt
from pytz import utc

import storage
import logging

log = logging.getLogger("uvicorn")


def start_background_jobs():
    jobstore = SQLAlchemyJobStore(url=storage.SQLALCHEMY_DATABASE_URL)
    executor = AsyncIOExecutor()
    scheduler = AsyncIOScheduler(
        executors={"default": executor},
        jobstores={"default": jobstore},
        timezone=utc,
        event_loop=get_event_loop(),
    )
    scheduler.start()
    if len(scheduler.get_jobs(jobstore)) == 0:
        try:
            scheduler.add_job(minute_job, trigger="cron", id="minute_job", minute="*/1")
            scheduler.add_job(
                five_minute_job, trigger="cron", id="five_minute_job", minute="*/5"
            )
            scheduler.add_job(
                ten_minute_job, trigger="cron", id="ten_minute_job", minute="*/10"
            )
            scheduler.add_job(
                thirty_minute_job, trigger="cron", id="thirty_minute_job", minute="*/30"
            )
            scheduler.add_job(
                daily, trigger="cron", id="daily", minute=0, hour=0, day="*/1"
            )
            scheduler.add_job(
                weekly,
                trigger="cron",
                id="weekly",
                minute=0,
                hour=0,
                month="*/1",
                day_of_week="0",
            )
        except Exception:
            pass
    [scheduler.resume_job(x.id) for x in scheduler.get_jobs()]
    log.info("JobScheduler: started")


def minute_job():
    log.info("JobScheduler: minute job completed")
    pass


def five_minute_job():
    log.info("JobScheduler: 5 minute job completed")
    pass


def ten_minute_job():
    log.info("JobScheduler: 10 minute job completed")
    pass


def thirty_minute_job():
    log.info("JobScheduler: 30 minute job completed")
    pass


def daily():
    log.info("JobScheduler: daily job completed")
    pass


def weekly():
    log.info("JobScheduler: weekly job completed")
    pass
