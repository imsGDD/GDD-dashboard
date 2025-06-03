# myapp/management/commands/import_damage_reports.py
from django.core.management.base import BaseCommand, CommandError
from dashboard_api.models import DamageReport, ChartData
import csv
import os
from django.db import transaction
from datetime import datetime

class Command(BaseCommand):
    help = 'Updates DamageReport and ChartData entries from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing the updates')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'File "{csv_file_path}" does not exist.')

        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:
                cards_column = row.get('cards')
                damage_or_name = row.get('damage/name').split('/')
                damage = damage_or_name[0]  # For DamageReport
                name = damage_or_name[1] if len(damage_or_name) > 1 else None  # For ChartData

                if 'HEADER' in cards_column:
                    # This row is for updating DamageReport
                    try:
                        with transaction.atomic():
                            damage_report, created = DamageReport.objects.update_or_create(
                                damage=damage,
                                defaults={
                                    'damage_value_percentage': row.get('damage_value_percentage/percentage'),
                                    'damage_value_number': row.get('damage_value_number/number'),
                                    # 'updated_at': datetime.strptime(row.get('updated_at/updated_at'), '%Y-%m-%d').date(),
                                }
                            )
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error updating DamageReport: {e}'))
                elif name:
                    # This row is for updating ChartData
                    try:
                        chart_data_qs = ChartData.objects.filter(
                            name=name
                        )

                        for chart_data in chart_data_qs:
                            # updated_at_raw = row.get('updated_at/updated_at') if 'updated_at/updated_at' in row and '/' in row.get('updated_at/updated_at') else None
                            # try:
                            #     updated_at = datetime.strptime(updated_at_raw, '%Y-%m-%d').date() if updated_at_raw else None
                            # except ValueError:
                            #     self.stdout.write(self.style.WARNING(f'Skipping row due to invalid date format: {updated_at_raw}'))
                            #     continue  # Skip this row and continue with the next one

                            chart_data.percentage = row.get('damage_value_percentage/percentage')
                            chart_data.number = int(row.get('damage_value_number/number'))  # Assuming this is always an integer
                            chart_data.save()
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error updating ChartData: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully updated DamageReport and ChartData based on file "{csv_file_path}"'))
