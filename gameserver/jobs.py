from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from datetime import datetime as dt
from pytz import utc

import storage



def start_background_jobs():
	jobstore = SQLAlchemyJobStore(url=storage.SQLALCHEMY_DATABASE_URL)
	executor = AsyncIOExecutor()
	scheduler = AsyncIOScheduler(executors=[executor], jobstores=[jobstore], timezone=utc)
	scheduler.start()
	if len(scheduler.get_jobs(jobstore)) == 0:
		scheduler.add_job(minute_job, trigger="cron", id='minute_job', minute='*/1')
		scheduler.add_job(ten_minute_job, trigger="cron", id='ten_minute_job', minute='*/10')
		scheduler.add_job(thirty_minute_job, trigger="cron", id='thirty_minute_job', minute='*/30')
		scheduler.add_job(daily, trigger="cron", id="daily", day="*/1")

def minute_job():
	pass

def ten_minute_job():
	pass

def thirty_minute_job():
	pass

def daily():
	pass