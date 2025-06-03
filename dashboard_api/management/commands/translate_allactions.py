import re
from django.core.management.base import BaseCommand
from dashboard_api.models import Action ,ChildAction

def normalize_numbers(text):
    """Removes commas from numbers in the text for consistent processing."""
    if text is None:
        return None  # Return None if the text is None
    return re.sub(r'(\d+),(\d+)', r'\1\2', text)
def extract_numbers(text):
    """Extracts all numbers from the given text."""
    if text is None:
        return []  # Return an empty list if text is None
    return re.findall(r'\d+', text)

def update_numbers(original_text, target_text):
    """Updates numbers in the target text based on the original text."""
    original_numbers = extract_numbers(original_text)
    target_numbers = extract_numbers(target_text)

    for original, target in zip(original_numbers, target_numbers):
        target_text = target_text.replace(target, original, 1)
    return target_text

# def format_numbers(text):
#     """Reformats numbers in the text to include commas as thousands separators."""
#     numbers = extract_numbers(text)
#     for number in numbers:
#         formatted_number = "{:,}".format(int(number))
#         text = text.replace(number, formatted_number, 1)
#     return text

class Command(BaseCommand):
    help = 'Updates damage summary'

    def handle(self, *args, **options):
        records = Action.objects.all()

        for record in records:
            action_type_ar = record.action_type_ar
            action_type_en = record.action_type_en
            action_type_tr = record.action_type_tr
            action_type_ind = record.action_type_ind

            # Normalize numbers by removing commas
            action_type_ar = normalize_numbers(action_type_ar)
            action_type_en = normalize_numbers(action_type_en)
            action_type_tr = normalize_numbers(action_type_tr)
            action_type_ind = normalize_numbers(action_type_ind)

            # Update numbers based on the Arabic summary
            updated_en = update_numbers(action_type_ar, action_type_en)
            updated_tr = update_numbers(action_type_ar, action_type_tr)
            updated_ind = update_numbers(action_type_ar, action_type_ind)

            # Format numbers to include commas
            # updated_en = format_numbers(updated_en)
            # updated_tr = format_numbers(updated_tr)
            # updated_ind = format_numbers(updated_ind)

            # Update the record
            record.action_type_en = updated_en
            record.action_type_tr = updated_tr
            record.action_type_ind = updated_ind
            record.save()

        self.stdout.write(self.style.SUCCESS('Update Translations Action completed.'))

        recordsChild = ChildAction.objects.all()

        for record in recordsChild:
            action_type_ar = record.action_type_ar
            action_type_en = record.action_type_en
            action_type_tr = record.action_type_tr
            action_type_ind = record.action_type_ind

            # Normalize numbers by removing commas
            action_type_ar = normalize_numbers(action_type_ar)
            action_type_en = normalize_numbers(action_type_en)
            action_type_tr = normalize_numbers(action_type_tr)
            action_type_ind = normalize_numbers(action_type_ind)

            # Update numbers based on the Arabic summary
            updated_en = update_numbers(action_type_ar, action_type_en)
            updated_tr = update_numbers(action_type_ar, action_type_tr)
            updated_ind = update_numbers(action_type_ar, action_type_ind)

            # Format numbers to include commas
            # updated_en = format_numbers(updated_en)
            # updated_tr = format_numbers(updated_tr)
            # updated_ind = format_numbers(updated_ind)

            # Update the record
            record.action_type_en = updated_en
            record.action_type_tr = updated_tr
            record.action_type_ind = updated_ind
            record.save()
        self.stdout.write(self.style.SUCCESS('Update Translations Child Action completed.'))



