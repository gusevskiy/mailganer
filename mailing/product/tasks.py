# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Mailing, MailingEmails
from celery import Celery
from django.conf import settings


@shared_task
def order_created(mailing_id):
    data = Mailing.objects.get(id=mailing_id)

    html_message = render_to_string(
        'patterns/form_one.html', {
        'header_email': data.header_email,
        'body_text': data.body_text,
        'sender_email': data.sender_email,
        }
    )

    for mail in data.mailing_emails.all():
        send_mail(
            subject=data.header_email,
            message=data.body_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[mail.email],
            html_message=html_message
        )
    