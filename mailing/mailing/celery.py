# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')
app = Celery('mailing',
    broker='redis://localhost:6379/0',  # Используй 'redis' если Celery внутри Docker, иначе 'localhost'
    backend='redis://redis:6379/0')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(['mailing'])


app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json'
)