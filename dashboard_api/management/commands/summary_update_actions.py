import csv
from django.core.management.base import BaseCommand
from dashboard_api.models import Sector, Costs, Summary
import re
import unicodedata

class Command(BaseCommand):
    help = 'Update data from CSV file into Django models'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    
    

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            

            for row in reader:
                sector_name = row['القطاع الرئيسي'].strip()
                sub_sector = row['القطاع الفرعي'].strip()



                sector = Sector.objects.filter(name__icontains=sector_name).first()


               

                # summary_obj= Summary.objects.get(sector=sector)
                # summary_obj.relief= row['relief'].replace(',', '')
                # summary_obj.recovery= row['recovery'].replace(',', '')
                # summary_obj.development= row['development'].replace(',', '')
                # summary_obj.total= row['total'].replace(',', '')
                # summary_obj.save()
        

                cost= Costs.objects.filter(sector=sector,sub_sector__icontains=sub_sector).first()
                #print(cost)    
                cost.damage_summary= row['ملخص الأضرار']
                cost.scope_of_intervention= row['أهم تدخلات الإغاثة والتعافي']
                cost.relief= row['الإغاثة'].replace(',', '')
                cost.recovery= row['التعافي'].replace(',', '')
                cost.development= row['التنمية'].replace(',', '')
                cost.total= row['الإجمالي'].replace(',', '')
                cost.save()
                


               

                self.stdout.write(self.style.SUCCESS(f'Successfully updated data for {sector_name} - {sub_sector}'))
