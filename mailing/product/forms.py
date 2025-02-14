# -*- coding: utf-8 -*-
from django import forms
import re
from .models import Mailing, MailingEmails

class MailingForm(forms.ModelForm):
    emails = forms.CharField(widget=forms.Textarea, help_text="Введите email-ы через запятую")
    
    class Meta:
        model = Mailing
        help_text = {
            'header_email': 'Заголовок/Приветствие',
            'body_text': 'Текст письма',
            'sender_email': 'Отправитель данного письма'
        }
        fields = ['header_email', 'body_text', 'sender_email']

    def clean_emails(self):
        """
        Валидатор (вызывается автоматически)
        проверяет соответствие кождого элемента списка
        email адресу.
        """
        # Преобразуем строку с email-ами в список
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        emails = self.cleaned_data['emails']
        email_list = [email.strip() for email in emails.split(',') if re.match(pattern, email)]
        return email_list
    
    def save(self, commit=True):
        mailing = super(MailingForm, self).save(commit=False)
        if commit:
            mailing.save()
        
        # Сохраняем каждый email как отдельную запись в MailingEmails
        email_list = self.cleaned_data['emails']
        for email in email_list:
            MailingEmails.objects.create(mailing=mailing, email=email)

        return mailing