import sqlite3
import re


def normalize_numbers(text):
    """Removes commas from numbers in the text for consistent processing."""
    return re.sub(r'(\d+),(\d+)', r'\1\2', text)


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


def format_numbers(text):
    """Reformats numbers in the text to include commas as thousands separators."""
    numbers = extract_numbers(text)
    for number in numbers:
        formatted_number = "{:,}".format(int(number))
        text = text.replace(number, formatted_number, 1)
    return text


# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Fetch all records that need updating from the dashboard_api_costs table
cursor.execute("""
    SELECT id, damage_summary_ar, damage_summary_en, damage_summary_tr, damage_summary_ind
    FROM dashboard_api_costs
""")
records = cursor.fetchall()

for record in records:
    id, damage_summary_ar, damage_summary_en, damage_summary_tr, damage_summary_ind = record

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
    updated_en = format_numbers(updated_en)
    updated_tr = format_numbers(updated_tr)
    updated_ind = format_numbers(updated_ind)

    # Prepare the update query
    update_query = """
    UPDATE dashboard_api_costs
    SET damage_summary_en = ?, damage_summary_tr = ?, damage_summary_ind = ?
    WHERE id = ?
    """

    # Execute the update query
    cursor.execute(update_query, (updated_en, updated_tr, updated_ind, id))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Update completed.")
