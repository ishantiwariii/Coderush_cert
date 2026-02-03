import os
import csv
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'certsite.settings') # Replace with your project name
django.setup()

from certificates.models import Participant # Replace with your actual app name

def import_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        skipped = 0
        
        for row in reader:
            email = row['Email'].strip()
            name = row['Full Name'].strip()
            # Mapping "Participant" from CSV to the model's "participant" choice
            position = 'participant' 

            # Using update_or_create to prevent duplicate email errors
            obj, created = Participant.objects.update_or_create(
                email=email,
                defaults={
                    'name': name,
                    'position': position,
                }
            )
            
            if created:
                count += 1
            else:
                skipped += 1
                
        print(f"Successfully imported {count} new participants.")
        print(f"Updated {skipped} existing participants.")

if __name__ == "__main__":
    import_csv('coderush_participants.csv')