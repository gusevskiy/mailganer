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

        tracking_url_subscribed = "{}{}".format(settings.SITE_URL, reverse('createmailing:track_email_subscribed', args=[mailing_log.tracking_id]))
        # экранирование спец символов в url
        tracking_url_subscribed = escape(tracking_url_subscribed)

        tracking_url_unsubscribed = "{}{}".format(settings.SITE_URL, reverse('createmailing:track_email_unsubscribed', args=[mailing_log.tracking_id]))
        # экранирование спец символов в url
        tracking_url_unsubscribed = escape(tracking_url_unsubscribed)


        
        # logging.info('Обратный url {}'.format(tracking_url))

        html_message = render_to_string(
            'patterns/form_one.html', {
            'header_email': data.header_email,
            'body_text': data.body_text,
            'tracking_url_subscribed': tracking_url_subscribed,
            'tracking_url_unsubscribed': tracking_url_unsubscribed,
            }
        )
        send_mail(
            subject=data.header_email,
            message=data.body_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[mail.email],
            html_message=html_message
        )
    