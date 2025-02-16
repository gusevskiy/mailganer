# -*- coding: utf-8 -*-
import pytz
import sys
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
import logging
from django.utils import timezone
from createmailing.models import MailingEmails
from .forms import MailingForm
from .tasks import order_created
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def create_order(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            date_completion = form.cleaned_data['date_completion']
     
            mailing = form.save()

            if date_completion:
                # Создаем отложенную задачу
                order_created.apply_async(
                    args=[mailing.id],
                    eta=date_completion
                )
            else:
                # Создаем задачу с исполнением сейчас
                order_created.apply_async(
                    args=[mailing.id]
                )
            return JsonResponse({'success': True})
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [unicode(error) for error in error_list]
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = MailingForm()
    return render(request, 'includes/create_order.html', {'form': form})


def test(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save()
            order_created.apply_async(args=[mailing.id])
            return HttpResponse("Order created and email sent!")
    else:
        form = MailingForm()
    return render(request, 'includes/test.html', {'form': form})


def track_email_subscribed(request, tracking_id):
    """
    Обновление статуса открытия письма получателем
    те если получатель открыл письмо и нажал подписаться
    """
    mailing_log = get_object_or_404(MailingEmails, tracking_id=tracking_id)
    tz = pytz.timezone('UTC')
    mailing_log.subscribed = True
    mailing_log.opened_at  = datetime.now(tz)
    mailing_log.save()
    logger.info("Отписались email {}".format(tracking_id))
    return HttpResponse("Вы успешно подписались на рассылки")

    
def track_email_unsubscribed(request, tracking_id):
    """
    Обновление статуса открытия письма получателем
    те если получатель открыл письмо и нажал отписаться
    """
    mailing_log = get_object_or_404(MailingEmails, tracking_id=tracking_id)
    tz = pytz.timezone('UTC')
    mailing_log.unsubscribed = True
    mailing_log.opened_at  = datetime.now(tz)
    mailing_log.save()
    logger.info("Отписались email {}".format(tracking_id))
    return HttpResponse("Вы успешно отписались от рассылки")
