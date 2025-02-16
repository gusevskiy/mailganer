# -*- coding: utf-8 -*-
import uuid
from django.db import models


class Mailing(models.Model):
    header_email = models.CharField(max_length=255, blank=False, null=False, verbose_name='Заголовок письма')
    body_text = models.TextField(blank=False, null=False,  verbose_name='Тело письма')
    sender_email = models.EmailField(blank=False, null=False,verbose_name='Отправитель письма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания рассылки')
    date_completion = models.DateTimeField(blank=False, null=False, verbose_name='Дата исполнения(запуска) рассылки')
    
    def __str__(self):
        return "Рассылка: {} - {} {}".format(self.id, self.sender_email, self.created_at)

class MailingEmails(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing_emails')
    email = models.EmailField()
    subscribed = models.BooleanField(default=False,  verbose_name='Подписался')
    unsubscribed = models.BooleanField(default=False, verbose_name='Отписался')
    opened_at = models.DateTimeField(null=True, blank=True, verbose_name='Когда открыто')
    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='трек номер почты')
    

    def __str__(self):
        return "Данные: {} - {}".format(self.id, self.email)

