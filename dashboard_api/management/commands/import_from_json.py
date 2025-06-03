# your_app_name/management/commands/import_data.py
import json
from django.core.management.base import BaseCommand
from dashboard_api.models import Action, ChildAction, Tag, Sector



class Command(BaseCommand):
    help = 'Import data from JSON file into Django models'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

        # ...
    def handle(self, *args, **options):
        json_file_path = options['json_file']

        with open(json_file_path, encoding='utf-8') as f:
            data = json.load(f)

            for item in data:
                # Your existing code for processing each item
                sector, created = Sector.objects.get_or_create(id=4, defaults={'name': 'Default Sector'})

                action_value = item.get('action_value', 0)

                try:
                    # Attempt to convert action_value to float
                    action_value = float(action_value)
                except (ValueError, TypeError):
                    # Handle cases where action_value is not a valid number
                    action_value = 0

                action_total = item.get('total', 0)
                try:
                    action_total = float(action_total)
                except (ValueError, TypeError):
                    action_total = 0 


                value = item.get('finished', 0)
                try:
                    finished_value = value
                except (ValueError, TypeError):
                    finished_value = 0   

                value = item.get('finished_percentage', 0)
                try:
                    finished_percentage_value = value
                except (ValueError, TypeError):
                    finished_percentage_value = 0          


                action = Action.objects.create(
                    key=item['key'],
                    sector=sector,
                    damage=item['damage'],
                    sub_sector=item['sub_sector'],
                    subclassification=item['subclassification'],
                    target_number=item['target_number'],
                    total_estimation=item['total_estimation'],
                    action_type=item['action_type'],
                    action_value=action_value,
                    total=action_total,
                    finished=finished_value,
                    finished_percentage=finished_percentage_value,
                )

                tags = [Tag.objects.get_or_create(name=tag)[0] for tag in item['tags']]
                action.tags.set(tags)

                self.stdout.write(self.style.SUCCESS(f'Successfully created Action: {action}'))

                for child_item in item.get('children', []):
                    child_action_value = child_item.get('action_value', 0)

                    try:
                        child_action_value = float(child_action_value)
                    except (ValueError, TypeError):
                        child_action_value = 0


                    child_total = child_item.get('total', 0)
                    try:
                        child_total = float(child_total)
                    except (ValueError, TypeError):
                        child_total = 0    

                    child_action = ChildAction.objects.create(
                        parent_action=action,
                        key=child_item['key'],
                        target_number=child_item['target_number'],
                        total_estimation=child_item['total_estimation'],
                        action_type=child_item['action_type'],
                        action_value=child_action_value,
                        total=child_total,
                        finished=None,
                        finished_percentage=None,
                    )

                    child_tags = [Tag.objects.get_or_create(name=tag)[0] for tag in child_item.get('tags', [])]
                    child_action.tags.set(child_tags)

                    self.stdout.write(self.style.SUCCESS(f'Successfully created ChildAction: {child_action}'))
    # ...
