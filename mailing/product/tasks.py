# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from celery import Celery


@shared_task
def order_created(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = "Order nr. {}".format(order_id)
        message = "Dear {},\n\nYou have successfully placed an order.\nYour order ID is {}.".format(order.first_name, order.id)
        mail_send = send_mail(subject, message, "ImRobotBender@yandex.ru", [order.email])

        return mail_send
    except Order.DoesNotExist:
        print("Order with id {} does not exist.".format(order_id))
        return None