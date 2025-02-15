# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Mailing, MailingEmails
from subscriber.models import Subscriber
from celery import Celery
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.html import escape
import logging


logger = logging.getLogger(__name__)


@shared_task
def order_created(mailing_id):
    data = Mailing.objects.get(id=mailing_id)


    for mail in data.mailing_emails.all():

        mailing_log = MailingEmails.objects.create(mailing=data, email=mail.email)

        tracking_url = "{}{}".format(settings.SITE_URL, reverse('createmailing:track_email_open', args=[mailing_log.tracking_id]))
        # экранирование спец символов в url
        tracking_url = escape(tracking_url)
        
        logging.info('Обратный url {}'.format(tracking_url))

        html_message = render_to_string(
            'patterns/form_one.html', {
            'header_email': data.header_email,
            'body_text': data.body_text,
            'sender_email': data.sender_email,
            'tracking_url': tracking_url,
            }
        )
        send_mail(
            subject=data.header_email,
            message=data.body_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[mail.email],
            html_message=html_message
        )
    