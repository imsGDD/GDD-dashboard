import re
from django.core.management.base import BaseCommand
from main.models import News

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



class Command(BaseCommand):
    help = 'Updates damage summary'

    def handle(self, *args, **options):
        records = News.objects.all()

        for record in records:
            news_ar = record.news_ar
            news_en = record.news_en
            news_tr = record.news_tr
            news_ind = record.news_ind

            # Normalize numbers by removing commas
            news_ar = normalize_numbers(news_ar)
            news_en = normalize_numbers(news_en)
            news_tr = normalize_numbers(news_tr)
            news_ind = normalize_numbers(news_ind)

            # Update numbers based on the Arabic summary
            updated_en = update_numbers(news_ar, news_en)
            updated_tr = update_numbers(news_ar, news_tr)
            updated_ind = update_numbers(news_ar, news_ind)

            # Format numbers to include commas
            # updated_en = format_numbers(updated_en)
            # updated_tr = format_numbers(updated_tr)
            # updated_ind = format_numbers(updated_ind)

            # Update the record
            record.news_en = updated_en
            record.news_tr = updated_tr
            record.news_ind = updated_ind
            record.save()

        self.stdout.write(self.style.SUCCESS('Update Translations Action completed.'))

       


