import csv
import slugify
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for row in phones:
            phone = Phone(
                id=int(row['id']),
                name=row['name'],
                price=int(row['price']),
                image=row['image'],
                release_date=row['release_date'],
                lte_exists=row['lte_exists'] == 'True',
                slug=slugify(row['name']),
            )
            phone.save()

