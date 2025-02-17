# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Mailing, MailingEmails
from subscriber.models import Subscriber


class MailingEmailsInline(admin.TabularInline):
    model = MailingEmails
    extra = 1


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    # поля, которые будут отображаться в списке объектов
    list_display = ('id', 'created_at', 'date_completion')
    # фильтры, которые будут доступны в правой части интерфейса.
    list_filter = ('created_at', 'date_completion')
    # поля, по которым можно будет искать объекты.
    search_fields = ('header_email', )
    # сортировка объектов в списке.
    ordering = ('-created_at', )  # Сортировка по дате создания (новые сверху)
    # связь, для отображения связаных обьектов
    inlines = [MailingEmailsInline]


@admin.register(MailingEmails)
class MailingEmailsAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'email', 'subscribed', 'unsubscribed',
                    'opened_at')
    list_filter = ('subscribed', 'unsubscribed', 'opened_at')
    search_fields = ('email', 'mailing__header_email')
    raw_id_fields = ('mailing', )  # Удобно для выбора связанной рассылки


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'birth_date',
                    'created_at')
    list_filter = ('last_name', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
