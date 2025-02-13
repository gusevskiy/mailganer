# -*- coding: utf-8 -*-
from django import forms
from .models import Mailing, MailingEmails

class MailingForm(forms.ModelForm):
    emails = forms.CharField(widget=forms.Textarea, help_text="Введите email-ы через запятую")
    
    class Meta:
        model = Mailing
        fields = ['header_email', 'body_text', 'sender_email']

    def clean_emails(self):
        # Преобразуем строку с email-ами в список
        emails = self.cleaned_data['emails']
        email_list = [email.strip() for email in emails.split(',')]
        return email_list
    
    def save(self, commit=True):
        mailing = super(MailingForm, self).save(commit=False)
        if commit:
            mailing.save()
        
        # Сохраняем каждый email как отдельную запись в MailingLog
        email_list = self.cleaned_data['emails']
        for email in email_list:
            MailingEmails.objects.create(mailing=mailing, email=email)

        return mailing