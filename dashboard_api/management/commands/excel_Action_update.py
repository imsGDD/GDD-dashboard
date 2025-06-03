# myapp/management/commands/update_actions.py
from django.core.management.base import BaseCommand, CommandError
from dashboard_api.models import Action, ChildAction
import pandas as pd


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
            c=0
            for index, row in df.iterrows():
                
                # Assuming column positions are the same as before
                damage = row.iloc[5]
                action_type = row.iloc[9]
                #print(f"damage is {damage} ---  {action_type} ")

                action = Action.objects.filter(damage__contains=damage,action_type__contains=action_type).first()
               
                if action is None:
                    # If action not found in Action model, find it in ChildAction model
                    action = ChildAction.objects.filter(parent_action__damage__contains=damage, action_type__contains=action_type).first()
                
                if action is not None:
                    c += 1                            
                    print(f"actions is=== {action}")
                    action.target_number = float(row.iloc[11]) if row.iloc[11] else action.target_number
                    action.total_estimation = float(row.iloc[8]) if row.iloc[8] else action.total_estimation
                    action.action_value = float(row.iloc[12]) if row.iloc[12] else action.action_value
                    action.total = float(row.iloc[13]) if row.iloc[13] else action.total
                    action.action_type = row.iloc[9]

                    action.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated data for {action} '))
                                                    
            print(c)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error updating entries: {e}'))

