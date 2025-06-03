

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
                damage = row.get('الأضرار')
                sub_sector = row.get('القطاع الفرعي')
                damage_value_number = row.get('تقدير الأضرار')
                damage_value_percentage = row.get('النسبة')

                updated_at = row.get('تاريخ تحديث المعلومة')
                updated_at = datetime.strptime(updated_at, '%Y-%m-%d').date() if updated_at else None
                damage_report = DamageReport.objects.filter(sub_sector=sub_sector, damage=damage).first()

                try:
                    with transaction.atomic():
                        if damage_report:
                            damage_report.updated_at=updated_at
                            # Handle damage_value_number
                            if damage_value_number and damage_value_number.isdigit():
                                damage_report.damage_value_number = int(damage_value_number)
                            elif damage_value_number:
                                damage_report.damage_value_number = float(damage_value_number.replace(',', '').replace('%', ''))
                            # Handle damage_value_percentage
                            if damage_value_percentage and damage_value_percentage.isdigit():
                                damage_report.damage_value_percentage = int(damage_value_percentage)
                            elif damage_value_percentage:
                                damage_report.damage_value_percentage = float(damage_value_percentage.replace(',', '').replace('%', ''))
                            damage_report.save()
                        else:
                            chart_data = ChartData.objects.filter(name=damage).first()
                            if chart_data:
                                chart_data.updated_at=updated_at
                                # Handle damage_value_number
                                if damage_value_number and damage_value_number.isdigit():
                                    chart_data.number = int(damage_value_number)
                                elif damage_value_number:
                                    chart_data.number = float(damage_value_number.replace(',', '').replace('%', ''))
                                # Handle damage_value_percentage
                                if damage_value_percentage and damage_value_percentage.isdigit():
                                    chart_data.percentage = int(damage_value_percentage)
                                elif damage_value_percentage:
                                    chart_data.percentage = float(damage_value_percentage.replace(',', '').replace('%', ''))
                                chart_data.save()
                            else:
                                # chart_data = ChartData.objects.create(name=damage)
                                # data_type=row.get('نوع القيمة (عدد، معدل، قيمة مالية)')

                                # chart_data.data_type=data_type
                                # chart_data.updated_at=updated_at

                                # if damage_value_number and damage_value_number.isdigit():
                                #     chart_data.number = int(damage_value_number)
                                # elif damage_value_number:
                                #     chart_data.number = float(damage_value_number.replace(',', '').replace('%', ''))
                                # # Handle damage_value_percentage
                                # if damage_value_percentage and damage_value_percentage.isdigit():
                                #     chart_data.percentage = int(damage_value_percentage)
                                # elif damage_value_percentage:
                                #     chart_data.percentage = float(damage_value_percentage.replace(',', '').replace('%', ''))
                                # chart_data.save()

                                self.stderr.write(self.style.ERROR(f'ChartData entry not found for damage: {damage}'))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error updating entries: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully updated DamageReport and ChartData based on file "{csv_file_path}"'))
