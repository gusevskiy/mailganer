# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2025-02-15 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(max_length=50, verbose_name='\u0418\u043c\u044f')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0438')),
            ],
        ),
    ]
