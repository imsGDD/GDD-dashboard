
import pandas as pd
from django.core.management.base import BaseCommand
from dashboard_api.models import DamageReport, ChartData
from django.db import transaction
from datetime import datetime
import math

class Command(BaseCommand):
    help = 'Updates DamageReport and ChartData entries from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')
        parser.add_argument('sheet_name', type=str, help='Name of the sheet to read data from')

    def handle(self, *args, **options):
        excel_file_path = options['excel_file']
        sheet_name = options['sheet_name']

        try:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
            c = 0
            for index, row in df.iterrows():
                damage = row.iloc[5]
                sub_sector = row.iloc[3]
                damage_value_number = row.iloc[8]
                damage_value_percentage = row.iloc[9]
                updated_at = row.iloc[6]

                #updated_at = datetime.strptime(updated_at, '%Y-%m-%d').date() if isinstance(updated_at, str) else None
                damage_report = DamageReport.objects.filter(sub_sector=sub_sector, damage=damage).first()

                if damage_report is None:
                    c += 1

                with transaction.atomic():
                    if damage_report:
                        damage_report.key=damage_report.id
                        damage_report.updated_at = updated_at
                        if not math.isnan(damage_value_number):
                            damage_report.damage_value_number = damage_value_number
                        if not math.isnan(damage_value_percentage):
                            damage_report.damage_value_percentage = '{:.2%}'.format(damage_value_percentage)
                        damage_report.save()
                    else:
                        chart_data = ChartData.objects.filter(name=damage).first()
                        if chart_data:
                            chart_data.updated_at = updated_at
                            if not math.isnan(damage_value_number):
                                if row.iloc[7] =="نسبة":
                                    print(damage_value_number)
                                    chart_data.number = '{:.2%}'.format(damage_value_number)
                                    chart_data.save()
                                else:
                                    chart_data.number = damage_value_number
                                    chart_data.save()

                            if not math.isnan(damage_value_percentage):
                                chart_data.percentage = '{:.2%}'.format(damage_value_percentage)
                            chart_data.save()
                        else:
                            self.stderr.write(self.style.ERROR(f'ChartData entry not found for damage: {damage}'))

            print(c)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error updating entries: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully updated DamageReport and ChartData based on file "{excel_file_path}"'))
