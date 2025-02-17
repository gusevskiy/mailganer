# -*- coding: utf-8 -*-
import json
import io

from django.core.management.base import BaseCommand

from subscriber.models import Subscriber


class Command(BaseCommand):
    help = ' Загрузить данные в модель ингредиентов '
    def handle(self, *args, **options):
        path_json = r'mailing/data/subscriber.json'
        self.stdout.write(self.style.WARNING(u'Старт команды'))
        with io.open(path_json) as data_file:
            data = json.loads(data_file.read())
            for i in data:
                Subscriber.objects.get_or_create(**i)

        self.stdout.write(self.style.SUCCESS(u'Данные загружены'))