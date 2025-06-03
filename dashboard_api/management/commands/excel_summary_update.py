

import pandas as pd
from django.core.management.base import BaseCommand
from dashboard_api.models import Sector, Costs, Summary
import re
import unicodedata

class Command(BaseCommand):
    help = 'Update data from Excel file into Django models'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')
        parser.add_argument('sheet_name', type=str, help='Name of the sheet to read data from')

    def handle(self, *args, **options):
        excel_file_path = options['excel_file']
        sheet_name = options['sheet_name']

        try:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
            for index, row in df.iterrows():
                # Assuming column positions are the same as before
                sector_name = row.iloc[1]
                sub_sector = row.iloc[2]

                print(sector_name)

                sector = Sector.objects.filter(name__icontains=sector_name).first()

                cost = Costs.objects.filter(sector=sector, sub_sector__icontains=sub_sector).first()
                if cost:
                    cost.damage_summary = row.iloc[3]
                    cost.scope_of_intervention = row.iloc[4]
                    cost.relief = str(row.iloc[5]).replace(',', '')
                    cost.recovery = str(row.iloc[6]).replace(',', '')
                    cost.development = str(row.iloc[7]).replace(',', '')
                    cost.total = str(row.iloc[8]).replace(',', '')
                    cost.save()
                    print(f"good  {cost}")

                    self.stdout.write(self.style.SUCCESS(f'Successfully updated data for {sector_name} - {sub_sector}'))
                else:
                    self.stderr.write(self.style.ERROR(f'Costs entry not found for sector: {sector_name}, sub-sector: {sub_sector}'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error updating entries: {e}'))

