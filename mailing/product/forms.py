# -*- coding: utf-8 -*-
from django import forms
import re
from .models import Mailing, MailingEmails
from django.conf import settings

class MailingForm(forms.ModelForm):
    header_email = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows':1}),
        label="Заголовок/Приветствие",
        required=False,
    )
    body_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows':5}),
        label="Текст письма",
        required=False
    )
    sender_email = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        label="Отправитель данного письма",
        required=False
    )
    emails = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        label="Введите email-ы через запятую",
        required=False
    )

    class Meta:
        model = Mailing
        fields = ['header_email', 'body_text', 'sender_email', 'emails']
        help_texts = {
            'header_email': 'Заголовок'
        }

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
    
    def clean_sender_email(self):
        data = self.cleaned_data['sender_email']
        if data:
            if re.match(settings.PATTERN, data):
                return data
            raise forms.ValidationError('Введите коректный адрес')


    def clean_emails(self):
        """
        Валидатор (вызывается автоматически)
        проверяет соответствие кождого элемента списка
        email адресу.
        """
        # Преобразуем строку с email-ами в список
        
        emails = self.cleaned_data['emails']
        if emails:
            email_list = [email.strip() for email in emails.split(',') if re.match(settings.PATTERN, email)]
            return email_list
        raise forms.ValidationError("Укажите адреса emailов на которые нужно отправить ваше письмо.")
    
    def save(self, commit=True):
        mailing = super(MailingForm, self).save(commit=False)
        if commit:
            mailing.save()
        
        # Сохраняем каждый email как отдельную запись в MailingEmails
        email_list = self.cleaned_data['emails']
        for email in email_list:
            MailingEmails.objects.create(mailing=mailing, email=email)

        return mailing
    