# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", blank=True, null=True)
    birth_date = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")
    
    def __str__(self):
        return "{} {} {}".format(self.first_name, self.last_name, self.email)
