# myapp/management/commands/update_actions.py
from hmac import new
from django.core.management.base import BaseCommand, CommandError
from dashboard_api.models import Action, ChildAction, Tag, Sector, Costs
import csv
import os
from django.db.models import Q

import csv
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from dashboard_api.models import Action

class Command(BaseCommand):
    help = 'Updates Action entries from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing the updates')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError(f'File "{csv_file_path}" does not exist.')

        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            #print(f"action is   {reade}")

            for row in reader:
                #actions = Action.objects.filter(damage__contains=row['subclassification'],action_type__contains=row['damage'])
                costs = Costs.objects.filter(scope_of_intervention__contains=row['scope_of_intervention'],sub_sector__contains=row['sub_sector'])

                
                print(f"actions is=== {costs}")
                

                for cost in costs:
                    # convert development, recovery, relief, total to float from (3,795,519,400)
                    development_new_float = float(row['development'].replace(',', '')) if row['development'] else cost.development
                    recovery_new_float = float(row['recovery'].replace(',', '')) if row['recovery'] else cost.recovery
                    relief_new_float = float(row['relief'].replace(',', '')) if row['relief'] else cost.relief
                    total_new_float = float(row['total'].replace(',', '')) if row['total'] else cost.total


                    cost.damage_summary = row['damage_summary'] if row['damage_summary'] else cost.damage_summary
                    # cost.recovery = float(row['total_estimation']) if row['total_estimation'] else cost.total_estimation
                    cost.development = development_new_float if development_new_float else cost.development
                    cost.recovery = recovery_new_float if recovery_new_float else cost.recovery
                    cost.relief =  relief_new_float if relief_new_float else cost.relief
                    cost.total = total_new_float if total_new_float else cost.total
                    cost.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated costs based on file "{csv_file_path}"'))
