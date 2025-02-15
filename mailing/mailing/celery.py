# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# from .settings import BROKER_URL, CELERY_RESULT_BACKEND

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')

app = Celery('mailing')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(["mailing"])

# app.conf.update(
#     BROKER_URL=BROKER_URL,
#     CELERY_RESULT_BACKEND=CELERY_RESULT_BACKEND,
#     CELERYBEAT_SCHEDULE={
#         'get_categories_every_one_minutes': {
#             'task': 'createmailing.tasks.order_created',
#             'schedule': crontab(minute='*/1'),
#         },
#     },
#     CELERY_TIMEZONE='UTC',
# )