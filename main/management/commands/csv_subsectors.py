import csv
from django.core.management.base import BaseCommand
from django.core.management.base import BaseCommand, CommandError

from main.models import Sectors,SubSectors
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
                sector_name = row['القطاعات']
                subsector_name = row['الأضرار  ']
                number = row['العدد']
                damage_percentage = row['نسبة الضرر']
                
                text = row['شرح التصميم']
                #print(f"sector name  {text}")
                sector= Sectors.objects.get(name=sector_name)
                #print(sector)
                #Create subsector under the sector
                SubSectors.objects.get_or_create(
                    main_sector=sector,
                    name=subsector_name,
                    number=number,
                    damage_percentage=damage_percentage,
                    text=text
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))