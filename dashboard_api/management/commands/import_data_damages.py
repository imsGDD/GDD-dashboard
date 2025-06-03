# myapp/management/commands/loaddata.py
import datetime
import json
from django.core.management.base import BaseCommand
from dashboard_api.models import DamageReport, Card, Chart, ChartData


# dashboard_api/management/commands/import_data_damages.py
import json
from django.core.management.base import BaseCommand
from dashboard_api.models import DamageReport, Card, Chart, ChartData
from datetime import date, datetime, timedelta


class Command(BaseCommand):
    help = 'Import data from JSON file into Django models'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:

                if item['updated_at'] :
                    try:
                        formatted_date = datetime.strptime(item['updated_at'], "%m/%d/%y").strftime("%Y-%m-%d")
                    except ValueError:
                        formatted_date = None #date.today()

                damage_report = DamageReport.objects.create(
                    #key=item['id'],
                    sector=item['sector'],
                    sub_sector=item['sub_sector'],
                    sub_classification=item['sub_classification'],
                    damage_sector=item['damage_sector'],
                    damage=item['damage'],
                    damage_value_type=item['damage_value_type'],
                    damage_value_number=item['damage_value_number'],
                    damage_value_percentage=item['damage_value_percentage'],
                    updated_at= formatted_date #datetime.strptime(item['updated_at'], '%m/%d/%y').strftime('%Y-%m-%d'),
                )

                for card_data in item['cards']:
                    if 'title' in card_data:
                        title = card_data['title'] 
                    else:
                        title = ' '
                    card = Card.objects.create(
                        damage_report=damage_report,
                        title=title,
                    )

                    for chart_data in card_data['charts']:
                        chart = Chart.objects.create(
                            card=card,
                            type=chart_data['type'],
                            #icon_code=chart_data['icon_code'],
                            icon_code=' '

                        )
                        

                        for data_point_data in chart_data['data']:
                            # if 'updated_at' in data_point_data:
                            #     #updated_at = datetime.strptime(data_point_data['updated_at'], '%m/%d/%y').strftime('%Y-%m-%d')
                            #     updated_at = data_point_data['updated_at']
                            # else:
                            #     updated_at = None
                            if data_point_data['updated_at']:
                                try:
                                    formatted_date = datetime.strptime(str(data_point_data['updated_at']), "%m/%d/%y").strftime("%Y-%m-%d")
                                except ValueError:
                                    # Handle the case where the date string is not in the expected format
                                    formatted_date = None#date.today()

                            try: 
                                number = int(data_point_data['number'])
                            except:
                                number = 0    

                            data_point = ChartData.objects.create(
                                chart=chart,
                                name=data_point_data['name'],
                                data_type=data_point_data['type'],
                                number=number,
                                percentage=data_point_data['percentage'],
                                updated_at=formatted_date
                                
                            )

        self.stdout.write(self.style.SUCCESS('Successfully imported data'))
