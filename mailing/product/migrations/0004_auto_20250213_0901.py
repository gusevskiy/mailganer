# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2025-02-13 09:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20250213_0852'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MailingLog',
            new_name='MailingEmails',
        ),
    ]
