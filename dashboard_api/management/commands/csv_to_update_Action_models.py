# myapp/management/commands/update_actions.py
from django.core.management.base import BaseCommand, CommandError
from dashboard_api.models import Action, ChildAction, Tag, Sector
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
                #print(f"damage is   {row}")
                # Using `icontains` for damage and subclassification to find matching entries
                #sub= row['subclassification'].split(' ')[0]
                #dam= row['damage'].split(' ')[0]
                #print(f"sub   {sub}   dam  {dam}")parent_action_damage__
                
                
                #actions = Action.objects.filter(damage__contains=row['subclassification'],action_type__contains=row['damage'])
                #actions = ChildAction.objects.filter(parent_action__damage__contains=row['subclassification'],action_type__contains=row['damage'])
                #actions = Action.objects.filter(damage__contains=row['الأضرار'],action_type__contains=row['نوع التدخل'])
                actions = ChildAction.objects.filter(parent_action__damage__contains=row['الأضرار'],action_type__contains=row['نوع التدخل'])


                
                print(f"actions is=== {actions}")
                
                

                for action in actions:
                    action.target_number = float(row['العدد المطلوب']) if row['العدد المطلوب'] else action.target_number
                    action.total_estimation = float(row['التقدير']) if row['التقدير'] else action.total_estimation
                    action.action_value = float(row['قيمة/تكلفة وحدة التدخل$']) if row['قيمة/تكلفة وحدة التدخل$'] else action.action_value
                    action.total = float(row['إجمالي التكلفة$']) if row['إجمالي التكلفة$'] else action.total
                    action.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated actions based on file "{csv_file_path}"'))
