from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from .download_from_api import *
import sys


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # save smog data form API every 10 minutes:
    scheduler.add_job(get_smog_data, 'interval', minutes=10)
    # save weather data form API every hour:
    scheduler.add_job(get_weather_data, 'interval', minutes=60)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))