from django.core.management.base import BaseCommand
from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import math
import datetime
from datetime import datetime


from main.models import Sectors,SubSectors,LastUpdated,Hero, News,SummaryTotal
import os
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
            for index, row in df.iterrows():
                sector_name = row.iloc[0]
                subsector_name = row.iloc[1]
                number = row.iloc[2]
                damage_percentage = row.iloc[3]
                
                text = row.iloc[5]
                #print(f"sector name  {text}")
                sector= Sectors.objects.get(name=sector_name)
                print(f"sector is {sector} dddd  {subsector_name}")
                #Create subsector under the sector
                subs,_=SubSectors.objects.get_or_create(main_sector=sector,name=subsector_name)
                print(f"subs is ---- {subs}")
                if not pd.isna(row.iloc[2]):
                    subs.number=number
                else:
                    subs.number=0

                if not pd.isna(row.iloc[3]):
                    subs.damage_percentage='{:.2%}'.format(damage_percentage)
                else:
                    subs.damage_percentage=0   
                subs.number=number 

                subs.damage_percentage= '{:.2%}'.format(damage_percentage)
                subs.text=text
                subs.save()
                
                self.stdout.write(self.style.SUCCESS(f'Successfully updated Subsectors '))
            
                if not pd.isna(row.iloc[7]):
                    sect = Sectors.objects.filter(name=row.iloc[7]).first()
                    sect.relief=row.iloc[8]
                    sect.recovery=row.iloc[9]
                    sect.development=row.iloc[10]
                    sect.save()
                        
                           
                     

                    self.stdout.write(self.style.SUCCESS('Successfully updated Sectors'))

                if not pd.isna(row.iloc[12]):
                    print(f"time is ---------{row.iloc[13]}")

                    lastupdate = LastUpdated.objects.get(id=1)
                    lastupdate.date= row.iloc[12]
                    #lastupdate.time= row.iloc[13]
                    lastupdate.time = datetime.strptime(row.iloc[13], '%H:%M:%S %p').time()

                    lastupdate.save()     
                            
                    self.stdout.write(self.style.SUCCESS('Successfully updated Time'))

                
                if not pd.isna(row.iloc[15]):    
                    hero = Hero.objects.get(name=row.iloc[15])
                    hero.number=row.iloc[16]
                    hero.save()


                    self.stdout.write(self.style.SUCCESS('Successfully updated Hero'))

               
                if not pd.isna(row.iloc[18]):
   
                    new= News.objects.get(id=1)
                                             
                    new.news= row.iloc[18]
                    new.days_of_genocide= row.iloc[19]
                    new.save()
                        
                    self.stdout.write(self.style.SUCCESS('Successfully updated News'))

                if not pd.isna(row.iloc[21]):
   
                    st= SummaryTotal.objects.get(id=1)
                    st.relief=row.iloc[21]
                    st.recovery=row.iloc[22]
                    st.development=row.iloc[23]                                             
                    st.total= row.iloc[24]
                    st.save()
                        
                    self.stdout.write(self.style.SUCCESS('Successfully Total Summary'))    


        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error updating entries: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully updated main page on file "{excel_file_path}"'))
