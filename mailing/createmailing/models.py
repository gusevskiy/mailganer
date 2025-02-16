# -*- coding: utf-8 -*-
import uuid
from django.db import models


class Mailing(models.Model):
    header_email = models.CharField(max_length=255, blank=False, null=False)
    body_text = models.TextField(blank=False, null=False)
    sender_email = models.EmailField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    date_completion = models.DateTimeField(blank=False, null=False)
    
    def __str__(self):
        return "Рассылка: {} - {} {}".format(self.id, self.sender_email, self.created_at)

class MailingEmails(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing_emails')
    email = models.EmailField()
    sent_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_opened = models.BooleanField(default=False)
    

    def __str__(self):
        return "Данные: {} - {}".format(self.id, self.email)


