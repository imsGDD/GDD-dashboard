import re
from django.core.management.base import BaseCommand
from dashboard_api.models import Costs  

def normalize_numbers(text):
    """Removes commas from numbers in the text for consistent processing."""
    pattern = re.compile(r'(\d+)[,\.](\d+)')
    normalized_text = re.sub(pattern, r'\1\2', text)
    return normalized_text

def extract_numbers(text):
    """Extracts all numbers from the given text."""
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
        records = Costs.objects.all()

        for record in records:
            damage_summary_ar = record.damage_summary_ar
            damage_summary_en = record.damage_summary_en
            damage_summary_tr = record.damage_summary_tr
            damage_summary_ind = record.damage_summary_ind

            # Normalize numbers by removing commas
            damage_summary_ar = normalize_numbers(damage_summary_ar)
            damage_summary_en = normalize_numbers(damage_summary_en)
            damage_summary_tr = normalize_numbers(damage_summary_tr)
            damage_summary_ind = normalize_numbers(damage_summary_ind)

            # Update numbers based on the Arabic summary
            updated_en = update_numbers(damage_summary_ar, damage_summary_en)
            updated_tr = update_numbers(damage_summary_ar, damage_summary_tr)
            updated_ind = update_numbers(damage_summary_ar, damage_summary_ind)

            # Format numbers to include commas
            # updated_en = format_numbers(updated_en)
            # updated_tr = format_numbers(updated_tr)
            # updated_ind = format_numbers(updated_ind)

            # Update the record
            record.damage_summary_en = updated_en
            record.damage_summary_tr = updated_tr
            record.damage_summary_ind = updated_ind
            record.save()

        self.stdout.write(self.style.SUCCESS('Update Translate completed.'))

