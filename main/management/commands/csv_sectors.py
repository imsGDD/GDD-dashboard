import csv
from django.core.management.base import BaseCommand
from django.core.management.base import BaseCommand, CommandError

from main.models import Sectors
import os
class Command(BaseCommand):
    help = 'Imports data from CSV to the database'
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing the updates')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'File "{csv_file_path}" does not exist.')

        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Assuming your model has fields matching the CSV columns
                obj, created = Sectors.objects.get_or_create(
                    key=row['القطاعات'],  # Assuming 'القطاعات' is unique
                    defaults={
                        'name': row['القطاعات'],  # Assuming 'القطاعات' is also the name
                        'relief': float(row['الإغاثة'].replace(',', '')),
                        'recovery': float(row['التعافي'].replace(',', '')),
                        'development': float(row['التنمية'].replace(',', ''))
                    }
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
