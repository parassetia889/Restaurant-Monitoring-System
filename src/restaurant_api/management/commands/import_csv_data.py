from django.utils import timezone
import os
from django.core.management.base import BaseCommand
import csv
from ...models import Store, BusinessHours, Timezones

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data")

STORE_INFO_CSV = os.path.join(CSV_PATH, "stores.csv")
STORE_HOURS_CSV = os.path.join(CSV_PATH, "buisness_hours.csv")
STORE_TIMEZONES_CSV = os.path.join(CSV_PATH, "time_zones.csv")


class Command(BaseCommand):
    help = "Import data from CSV files"

    def handle(self, *args, **options):
        # Import store_info.csv
        with open(STORE_INFO_CSV, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                try:
                    datetime_str = row[2].split(".")[0] + " UTC"
                    timestamp = timezone.datetime.strptime(
                        datetime_str, "%Y-%m-%d %H:%M:%S %Z"
                    )
                    timestamp_utc = timezone.make_aware(timestamp, timezone.utc)
                    Store.objects.create(
                        store_id=row[0], status=row[1], timestamp_utc=timestamp_utc
                    )
                except ValueError as e:
                    # Handle the error here, you can print the error message or log it
                    print(f"Error processing row: {e} {row[2]}  StoreId  {row[0]}")

        # # Import store_hours.csv
        with open(STORE_HOURS_CSV, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                try:
                    BusinessHours.objects.create(
                        store_id=row[0],
                        day=row[1],
                        start_time_local=row[2],
                        end_time_local=row[3],
                    )
                except ValueError as e:
                    # Handle the error here, you can print the error message or log it
                    print(f"Error processing row: {e} {row[2]}  StoreId  {row[0]}")

        # # Import store_timezones.csv
        with open(STORE_TIMEZONES_CSV, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                try:
                    Timezones.objects.create(
                        store_id=row[0],
                        timezone_str=row[1],
                    )
                except ValueError as e:
                    # Handle the error here, you can print the error message or log it
                    print(f"Error processing row: {e} {row[1]}  StoreId  {row[0]}")

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
