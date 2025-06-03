# import json
# from django.core.management.base import BaseCommand
# from dashboard_api.models import Sector, Costs, Summary


# class Command(BaseCommand):
#     help = 'Import data from JSON file into Django models'

#     def add_arguments(self, parser):
#         parser.add_argument('json_file', type=str, help='Path to the JSON file')

#     def handle(self, *args, **options):
#         json_file_path = options['json_file']
#         with open(json_file_path, 'r', encoding='utf-8') as file:
#             data = json.load(file)

#             for sector_data in data['data']:  
#                 sector_name = sector_data['sector']
#                 sector= Sector.objects.get(id=4)
                

#                 for item in sector_data['data']:
#                     cost = Costs.objects.create(
#                     sector=sector,
#                     sub_sector=item['sub_sector'],
#                     damage_summary=item['damage_summary'],
#                     scope_of_intervention=item['scope_of_intervention'],
#                     relief=item['relief'],
#                     recovery=item['recovery'],
#                     development=item['development'],
#                     total=item['total'],
#                     key=item['key'],  

#                 )
#                 summary_obj = Summary.objects.create(
#                     sector=sector,
#                     relief=sector_data['summary']['relief'],
#                     recovery=sector_data['summary']['recovery'],
#                     development=sector_data['summary']['development'],
#                     total=sector_data['summary']['total'],
#                 )
#             self.stdout.write(self.style.SUCCESS(f'Successfully imported {cost.sub_sector} into {sector.name}'))
import json
from django.core.management.base import BaseCommand
from dashboard_api.models import Sector, Costs, Summary

class Command(BaseCommand):
    help = 'Import data from JSON file into Django models'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for sector_data in data['data']:
                sector_name = sector_data['sector']
                sector= Sector.objects.get(id=4)

                summary_obj, created = Summary.objects.get_or_create(
                    sector=sector,
                    relief=sector_data['summary']['relief'],
                    recovery=sector_data['summary']['recovery'],
                    development=sector_data['summary']['development'],
                    total=sector_data['summary']['total'],
                )

                for item in sector_data['data']:
                    cost = Costs.objects.create(
                        sector=sector,
                        sub_sector=item['sub_sector'],
                        damage_summary=item['damage_summary'],
                        scope_of_intervention=item['scope_of_intervention'],
                        relief=item['relief'],
                        recovery=item['recovery'],
                        development=item['development'],
                        total=item['total'],
                        key=item['key'],
                    )
                    summary_obj.cost.add(cost)

                self.stdout.write(self.style.SUCCESS(f'Successfully imported data into {sector.name}'))
