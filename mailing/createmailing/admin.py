# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Mailing, MailingEmails


class MailingEmailsInline(admin.TabularInline):
    model = MailingEmails
    extra = 1 

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    # поля, которые будут отображаться в списке объектов
    list_display = ('id', 'sender_email', 'created_at', 'date_completion')
    # фильтры, которые будут доступны в правой части интерфейса.
    list_filter = ('created_at', 'date_completion')
    # поля, по которым можно будет искать объекты.
    search_fields = ('header_email', 'sender_email')
    # сортировка объектов в списке.
    ordering = ('-created_at',)  # Сортировка по дате создания (новые сверху)
    # связь, для отображения связаных обьектов
    inlines = [MailingEmailsInline]

@admin.register(MailingEmails)
class MailingEmailsAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'email', 'subscribed', 'unsubscribed', 'opened_at')
    list_filter = ('subscribed', 'unsubscribed', 'opened_at')
    search_fields = ('email', 'mailing__header_email')
    raw_id_fields = ('mailing',)  # Удобно для выбора связанной рассылки
