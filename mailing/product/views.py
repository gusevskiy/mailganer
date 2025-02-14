# -*- coding: utf-8 -*-
import pytz
import sys
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
import logging
from product.models import MailingEmails
from .forms import MailingForm
from .tasks import order_created
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


logger = logging.getLogger(__name__)


def create_order(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save()
            order_created.apply_async(args=[mailing.id])
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


def track_email_open(request, tracking_id):
    """
    Обновление статуса открытия письма получателем
    """
    mailing_log = get_object_or_404(MailingEmails, tracking_id=tracking_id)
    tz = pytz.timezone('UTC')
    mailing_log.is_opened = True
    mailing_log.opened_at  = datetime.now(tz)
    mailing_log.save()
    logger.info("Open email {}".format(tracking_id))
    return HttpResponse("Вы успешно отписались от рассылки")