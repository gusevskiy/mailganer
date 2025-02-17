# -*- coding: utf-8 -*-
from django import forms
import re
from .models import Mailing, MailingEmails
from subscriber.models import Subscriber
from django.conf import settings
import logging
from datetime import datetime, timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)


class MailingForm(forms.ModelForm):
    header_email = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 1
        }),
        label="Заголовок/Приветствие",
        required=False,
    )
    body_text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3
    }),
                                label="Текст письма",
                                required=False)
    emails = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3
    }),
                             label="Email-ы всех подписчиков.",
                             required=False)
    date_completion = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
        }),
        label="Дата и время",
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Mailing
        fields = ['header_email', 'body_text', 'emails', 'date_completion']

    def __init__(self, *args, **kwargs):
        """
        Подставляем emails в форму, их сразу видно.
        """
        super(MailingForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            subscriber_emails = Subscriber.objects.values_list('email',
                                                               flat=True)
            self.fields['emails'].initial = ', '.join(subscriber_emails)

    def clean_header_email(self):
        """
        Проверка ввода заголовка
        """
        data = self.cleaned_data['header_email']
        if data:
            return data
        raise forms.ValidationError("Заполните Заголовок/Приветствие.")

    def clean_body_text(self):
        """
        Проверка ввода текста письма
        """
        data = self.cleaned_data['body_text']
        if data:
            return data
        raise forms.ValidationError("Заполните текст письма.")

    def clean_emails(self):
        """
        Валидатор (вызывается автоматически)
        проверяет соответствие кождого элемента списка
        email адресу.
        """
        emails = self.cleaned_data['emails']
        if emails:
            email_list = []
            for email in emails.split(','):
                email = email.strip()
                match = re.match(settings.PATTERN, email)
                if match:
                    email_list.append(email)
            logging.info("list emails: {}".format(email_list))
            return email_list
        raise forms.ValidationError(
            "Укажите адреса emailов на которые нужно отправить ваше письмо.")

    def clean_date_completion(self):
        """
        Проверяет на прошедшее время
        Если время не указано возвращает текущие + 10 секунд
        (это для того чтобы в БД записалось время создания и время исполнения)
        """
        data = self.cleaned_data['date_completion']
        if data:
            # Преобразуем дату в осведомленное время, если она наивная
            # (наивная это без timezone, осведомленное с timezone)
            if timezone.is_naive(data):
                data = timezone.make_aware(data,
                                           timezone.get_current_timezone())
            # Проверка на уже прошедшую дату
            if data < timezone.now():
                raise forms.ValidationError(
                    'Дата выполнения уже прошла,измените время.')
            return data
        return datetime.now() + timedelta(seconds=10)

    def save(self, commit=True):
        """
        Добавляем к каждой рассылке, все входящие в нее emails
        """
        mailing = super(MailingForm, self).save(commit=False)
        if commit:
            mailing.save()

        # Сохраняем каждый email как отдельную запись в MailingEmails
        email_list = self.cleaned_data['emails']
        for email in email_list:
            MailingEmails.objects.create(mailing=mailing, email=email)

        return mailing
